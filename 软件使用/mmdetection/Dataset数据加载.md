## mmdetection 数据加载简介
mmdetection的数据加载使用pytorch的Dataset类进行，事先继承Dataset类并且定义好__getitem__方法，再使用dataloader进行加载。实际上由于要支持mixup等数据增强方法、多个数据集拼接等功能，mmdetection通过Dataset Wrapper对基础Dataset进行包装，实现了多种不同的数据加载方式，从mmdet.datasets.build_dataset方法中可以看到：
```python
def build_dataset(cfg, default_args=None):
    from .dataset_wrappers import (ConcatDataset, RepeatDataset,
                                   ClassBalancedDataset, MultiImageMixDataset)
    if isinstance(cfg, (list, tuple)):
        dataset = ConcatDataset([build_dataset(c, default_args) for c in cfg])
    elif cfg['type'] == 'ConcatDataset':
        dataset = ConcatDataset(
            [build_dataset(c, default_args) for c in cfg['datasets']],
            cfg.get('separate_eval', True))
    elif cfg['type'] == 'RepeatDataset':
        dataset = RepeatDataset(
            build_dataset(cfg['dataset'], default_args), cfg['times'])
    elif cfg['type'] == 'ClassBalancedDataset':
        dataset = ClassBalancedDataset(
            build_dataset(cfg['dataset'], default_args), cfg['oversample_thr'])
    elif cfg['type'] == 'MultiImageMixDataset':
        cp_cfg = copy.deepcopy(cfg)
        cp_cfg['dataset'] = build_dataset(cp_cfg['dataset'])
        cp_cfg.pop('type')
        dataset = MultiImageMixDataset(**cp_cfg)
    elif isinstance(cfg.get('ann_file'), (list, tuple)):
        dataset = _concat_dataset(cfg, default_args)
    else:
        dataset = build_from_cfg(cfg, DATASETS, default_args)

    return dataset
```
从代码中可以推测几种特殊Dataset Wrapper的功能：
ConcatDataset：拼接多个数据集
RepeatDataset：一个数据集重复指定次数
ClassBalancedDataset：均匀采样
MultiImageMixDataset：Mixup等数据增强方式
其他：自定义的Dataset，每次一张图及对应标签

## 基础类CustomDataset
定义于文件mmdet.datasets.custom.py,COCO等其他数据集的Dataset构建都继承自该类，该类的大部分方法都可以重新改写，依照不同的数据集的标注格式进行自定义。
基本的pipeline如下：
Dataset初始化，记录数据集图片、标注文件的根目录，并且使用load_annotations读取所有图片的data_info,后续读取每个条目就会从data_info入手，查找图片名和对应的标注内容。如果是预先计算好的proposal，需要调用load_proposals方法，加载proposal信息
__getitem__方法：
```python
    def __getitem__(self, idx):
        """Get training/test data after pipeline.

        Args:
            idx (int): Index of data.

        Returns:
            dict: Training/test data (with annotation if `test_mode` is set \
                True).
        """

        if self.test_mode:
            return self.prepare_test_img(idx)
        while True:
            data = self.prepare_train_img(idx) #调用get_ann_info函数获取图片对应的标注信息
            if data is None:
                idx = self._rand_another(idx)
                continue
            return data
```
训练和测试的区别在于是否获取标注文件的信息，具体地是否调用get_ann_info函数，二者的区别看代码：
```python
    def prepare_train_img(self, idx):
        """Get training data and annotations after pipeline.

        Args:
            idx (int): Index of data.

        Returns:
            dict: Training data and annotation after pipeline with new keys \
                introduced by pipeline.
        """

        img_info = self.data_infos[idx]
        ann_info = self.get_ann_info(idx)
        results = dict(img_info=img_info, ann_info=ann_info)
        if self.proposals is not None:
            results['proposals'] = self.proposals[idx]
        self.pre_pipeline(results)
        return self.pipeline(results)

    def prepare_test_img(self, idx):
        """Get testing data  after pipeline.

        Args:
            idx (int): Index of data.

        Returns:
            dict: Testing data after pipeline with new keys introduced by \
                pipeline.
        """

        img_info = self.data_infos[idx]
        results = dict(img_info=img_info)
        if self.proposals is not None:
            results['proposals'] = self.proposals[idx]
        self.pre_pipeline(results)
        return self.pipeline(results)
```
获取到图像和标注信息后，会调用pre_pipeline和pipeline进行预处理和数据增强，具体输出的数据格式，比如box是中心点+宽高还是tl坐标+br坐标，需要看get_ann_info的定义
