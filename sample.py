import cv2
import numpy as np
import os
try:
    import preprocess
except:
    print("not install preprocess from qingna")

def load_from_txt(line):
    line = line.strip().split(' ')
    num_res = (len(line) - 1)//13
    pred_res = [[], [], [], []]
    res_p = []
    res_v = []
    res = []
    if num_res == 0:
        return res
    else:
        for i in range(num_res):
            label = int(line[i*13 + 1])
            cls = int(line[i*13 + 2])
            score = float(line[i*13 + 13])
            box = line[i*13+3:i*13+14]
            obj = line[i*13 + 1:i*13+7]
            print(obj)
            res.append(obj)
    return res

def process(video):
    numVideo = video
    list_file = open('lst.txt',mode='w')
    res = open('./{}/nv/res.txt'.format(numVideo), mode='r')
    os.makedirs('{}/results'.format(numVideo),exist_ok=True)
    cur_frame = 0
    while 1:
        line = res.readline()
        print(cur_frame)
        print(line)
        if line =='\n' or line == '':
            break
        name = line.split(' ')[0]
        nv12_file='./{}/nv/{}'.format(numVideo,name)
        print('nv12_file:',nv12_file)
        nv12_data=np.fromfile(nv12_file,np.uint8)
        bgr_data=np.ndarray((3*1280*1920),dtype=np.uint8)
        preprocess.YUV4202BGR(nv12_data,bgr_data,1920,1280)
        img = np.reshape(bgr_data,(1280,1920,3))
        img=img.copy().astype(np.uint8)
        # img=img[:,:,::-1]
        # cv2.imwrite('img.jpg',img)
        # break
        print('img shape:',img.shape)
        outputs = load_from_txt(line)
        for obj in outputs:
            if int(obj[0])==4:
                cv2.rectangle(img, (int(obj[2]), int(obj[3])), (int(obj[4]), int(obj[5])), (0, 0, 255), 2)
            elif int(obj[0])==2:
                cv2.rectangle(img, (int(obj[2]), int(obj[3])), (int(obj[4]), int(obj[5])), (0, 255, 0), 2)
            else:
                cv2.rectangle(img, (int(obj[2]), int(obj[3])), (int(obj[4]), int(obj[5])), (255, 0, 0), 2)
        cur_frame = cur_frame + 1
        dst_name = nv12_file.replace('/nv','/results').replace('.i420','.jpg')
        print('dst_name:',dst_name)
        cv2.imwrite(dst_name,img)
    res.close()
def main():
    videos=['origin']
    for video in videos:
        process(video)


    
if __name__ == '__main__':
    main()
