import os
from pathlib import Path
import cv2
import numpy as np

img = cv2.imread(r'E:\database\adas\SelfTest\images\VD30620400066_20200604193012_01_0000000000000108_video_000345.png')
print(img.shape)
img = np.transpose(img,[1,2,0])
print(img.shape)
# root=Path(r'E:\共享\adas\motion-status\data\neg')
# txtfiles = list(root.glob('*.txt'))
# for file in txtfiles:
#     print(file)
#     with file.open('r') as fin:
#         lines = fin.readlines()
#     outFname=str(file).replace('.txt','_process.txt')
#     with open(outFname,'w') as fout:
#         for line in lines:
#             parts = line.split(' ')[1::2]
#             fout.write(' '.join(parts)+'\n')