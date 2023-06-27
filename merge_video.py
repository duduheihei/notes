import cv2
import numpy as np

cap0 = cv2.VideoCapture(r'E:\虹软\技术大会ppt\2022\old_version.avi')
cap1 = cv2.VideoCapture(r'E:\虹软\技术大会ppt\2022\new_version.avi')

# ovideo = cv2.VideoWriter(r'E:\虹软\技术大会ppt\2022\compare_video.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1920//2,1280//4))
ovideo = cv2.VideoWriter(r'E:\虹软\技术大会ppt\2022\compare_video.avi',-1, 30, (1920//2,1280//4))

while True:
    ret,img1 = cap0.read()
    ret,img2 = cap1.read()
    if img1 is None:
        break
    # img1 = cv2.resize(img1,(1920//4,1280//4))
    # img2 = cv2.resize(img2,(1920//4,1280//4))
    img1 = img1[640-1280//8:640+1280//8,960-1920//8:960+1920//8]
    img2 = img2[640-1280//8:640+1280//8,960-1920//8:960+1920//8]
    oimg = np.concatenate([img1,img2],axis=1)
    ovideo.write(oimg)

ovideo.release()
