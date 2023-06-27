import cv2
import os

with open(r'\\172.17.218.174\nfs_share\bqj7379\test_day\res_tricone.txt','r') as f:
    lines = f.readlines()

for line in lines:
    parts = line.strip().split(' ')
    name = parts[0]
    parts = parts[1:]
    img_name = os.path.join(r'E:\database\adas\qa\thin_cylinder',name.replace('.nv12','.jpg'))
    img = cv2.imread(img_name)
    for i in range(len(parts)//13):
        cat,subcat,l,t,r,b = parts[i*13:i*13+6]
        cv2.rectangle(img,(int(l),int(t)),(int(r),int(b)),(0,0,255),1,1)
    cv2.imshow('img',img)
    cv2.waitKey(0)

