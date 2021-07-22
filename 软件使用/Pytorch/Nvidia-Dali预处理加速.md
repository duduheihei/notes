## Dali
[官网](https://docs.nvidia.com/deeplearning/dali/user-guide/docs/index.html)

### 简要介绍
Dali提供了jpeg图片的解码算法，速度优于opencv，同时提供了一系列预处理算法包括crop、color_twist等，并且可以放在GPU上运算，解放cpu的计算瓶颈。对于常见数据集的读取，Dali提供了一系列reader，直接从文件夹或者hmdf文件读取，然后送入模型。对于视频任务，其也提供了方便的读取函数，但是对于解压后的帧，并且指定开始和结束帧，目前dali尚未计划实现该功能，具体见[github issue](https://github.com/NVIDIA/DALI/issues/3138#issuecomment-880682329)

### 代码
废话少说，直接上代码
```python
## Dali Version: 1.3.0
import nvidia.dali.fn as fn
from nvidia.dali import pipeline_def,Pipeline
import nvidia.dali.types as types
from nvidia.dali.plugin.pytorch import DALIGenericIterator
from nvidia.dali.plugin.pytorch import LastBatchPolicy
from nvidia.dali.types import DALIImageType


from pathlib import Path
import os
from sklearn.utils import shuffle
import random
import numpy as np
import cv2

class INPUT_ITER(object):
    def __init__(self, batch_size,seq_len, sample_rate, num_shards=1, shard_id=0,root_dir=Path('') ,list_file='', is_training=True):
        self.batch_size = batch_size
        self.seq_len = seq_len
        self.sample_rate = sample_rate
        self.num_shards = num_shards
        self.shard_id = shard_id
        self.train = is_training
        self.image_name_formatter = lambda x: f'image_{x:05d}.jpg'
        self.root_dir = root_dir
        with open(list_file,'r') as f:
            self.ori_lines = f.readlines()
        bucket = len(self.ori_lines)//self.num_shards
        self.n = bucket
        print("self.n = bucket is ",self.n)
        self.data_set_len  = self.n*self.num_shards


    def __iter__(self):
        self.i = 0
        # print("self.n = bucket is %i",self.n)
        if self.train:
            self.ori_lines = shuffle(self.ori_lines, random_state=0)
            self.ori_lines = shuffle(self.ori_lines, random_state=0)
        self.lines = self.ori_lines[self.shard_id*self.n:(self.shard_id+1)*self.n]
        return self
    
    def sample_indices(self):
        '''
        line = '揉眼睛/xxx start end label'
        '''
        line = self.lines[self.i].strip()
        dir_name,start_f,end_f, label = line.split(' ')
        start_f = int(start_f)
        end_f = int(end_f)
        label = int(label)
        begin_frame = random.randint(start_f,max(end_f-self.sample_rate*self.seq_len,start_f))
        begin_frame = max(1,begin_frame)
        indices = []
        for k in range(self.seq_len):
            if self.train:
                img_idx = begin_frame+self.sample_rate*k + random.randint(-1, 1)
            else:
                img_idx = begin_frame+self.sample_rate*k
            img_idx = max(1, img_idx)
            indices.append(img_idx)
        return dir_name,indices,label
    

    def __next__(self):
        batch = [[] for _ in range(self.seq_len)]
        batch_list = []
        labels = []
        for _ in range(self.batch_size):
            # self.sample_rate = random.randint(1,2)
            if self.i >= self.n:
                self.__iter__()
                raise StopIteration
                
            # print("##################################",line)
            dir_name,indices,label = self.sample_indices()
            last_frame = None
            for k,img_idx in enumerate(indices):
                filename = self.root_dir/dir_name/self.image_name_formatter(img_idx)
                if filename.exists():
                    f = open(filename,'rb')
                    last_frame = filename
                elif last_frame is not None:
                    f = open(last_frame,'rb')
                else:
                    print('{} does not exist'.format(filename))
                    raise IOError
                batch[k].append(np.frombuffer(f.read(), dtype = np.uint8))
                batch_list.append(batch[k][-1])
                # labels.append(np.array([label], dtype = np.uint8))
                f.close()
            # batch_list.append(batch[k][-1])
            labels.append(np.array([label], dtype = np.uint8))
            self.i = self.i + 1
        # return (batch[0],batch[1],batch[2],batch[3],batch[4],batch[5],batch[6],batch[7],batch[8],batch[9],\
        #     batch[10],batch[11],batch[12],batch[13],batch[14],batch[15],labels)
        # print('len(batch)',len(batch))
        return (*batch,labels)

    def __len__(self):
        return self.data_set_len
    
    next = __next__


def ExternalSourcePipeline(batch_size, num_threads, device_id, external_data,seq_len, size, is_grey, is_training = True):
    pipe = Pipeline(batch_size, num_threads, device_id,prefetch_queue_depth=2)
    with pipe:
        outputs = fn.external_source(source=external_data, num_outputs=seq_len+1)
        jpegs = outputs[:-1]
        labels = outputs[-1]
        
        if is_grey:
            images = fn.decoders.image(jpegs, device="mixed",output_type=DALIImageType.GRAY)
        else:
            images = fn.decoders.image(jpegs, device="mixed",output_type=DALIImageType.BGR)
        
        if is_training:
            # # color twist augmentation
            brightness = fn.random.uniform(range=(0.5, 1.5))
            contrast = fn.random.uniform(range=(0.5, 1.5))

            # # saturation does not show changes in grey, range in [0,1] 
            # # saturation  = fn.random.uniform(range=(0, 1))

            # # hue change does not show changes in grey images, official example usually set it to 45~120
            # # hue = fn.random.uniform(range=(-0.3, 0.3))

            # # color_twist can only process RGB/BGR
            if not is_grey:
                images = fn.color_twist(images,brightness=brightness, contrast = contrast)
            else:
                images = fn.brightness_contrast(images,brightness=brightness, contrast = contrast)

            # jitter , space augmentation,  Each pixel is moved by a random amount in the [-nDegree/2, nDegree/2] range
            # images = fn.jitter(images,nDegree=2)
            

            # angle rotation augmentation
            angle = fn.random.uniform(range=(-10.0, 10.0))
            images = fn.rotate(images, angle=angle, fill_value=0)

            # random crop resize while training
            images = fn.random_resized_crop(images,size=size,random_area=[0.7, 1.0],random_aspect_ratio=[0.7,1.3])
        else:
            # # center crop while test or validation
            # images = fn.random_resized_crop(images)

            images = fn.resize(images, size = size)
        

        
        images = fn.stack(*images)
        images = fn.reshape(images, layout="FHWC")

        images = fn.transpose(images,perm=[3,0,1,2], output_layout="FCHW")
        images = fn.cast(images, dtype=types.FLOAT)
        pipe.set_outputs(images,labels)
    return pipe


def get_dali_loader(root_dir,list_file,batch_size,seq_len,sample_rate,num_gpus,device_id,num_threads,size,is_gray,is_training=True):
    ext_source = INPUT_ITER(batch_size, seq_len, sample_rate, num_gpus, device_id,root_dir,list_file,is_training)
    pipe = ExternalSourcePipeline(batch_size, num_threads, device_id, ext_source,seq_len,size,is_gray,is_training)
    pii = DALIGenericIterator(pipe,['data','label'],last_batch_padded=True, last_batch_policy=LastBatchPolicy.PARTIAL)
    return pii
```