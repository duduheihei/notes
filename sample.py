import cv2

img = cv2.imread(r'T3_taxi01_hz_20210601_yuv_0000000041_0000002693_0000001950111.png')
center = (1280//2,720//2)
w = 448
h = 224
lt = (center[0]-w//2,center[1]-h//2+32)
br = (lt[0]+w-1,lt[1]+h-1)
cv2.circle(img,center,3,(255,0,0),3)
cv2.rectangle(img,lt,br,(0,255,0),3)

w = int(1024/1920*1280)
h = int(448/1280*720)
lt = (center[0]-w//2,center[1]-h//2+32)
br = (lt[0]+w-1,lt[1]+h-1)
cv2.rectangle(img,lt,br,(0,0,255),3)


# imgresize=cv2.resize(img,(1920//2,1280//2))
cv2.imshow('img',img)
cv2.imwrite(r'crop.jpg',img)
cv2.waitKey(0)

# cap = cv2.VideoCapture(r'D:\ProjectData\vpd\1665640743_0.h264')
# out_avi = cv2.VideoWriter(r'D:\ProjectData\vpd\crop.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1920//2,1280//2))
# while True:
#     ret,img = cap.read()
#     if img is None:
#         break
#     center = (940,650)
#     w = 448
#     h = 224
#     lt = (center[0]-w//2,center[1]-h//2)
#     br = (lt[0]+w-1,lt[1]+h-1)
#     cv2.circle(img,center,3,(255,0,0),3)
#     cv2.rectangle(img,lt,br,(0,255,0),3)

#     w = 1024
#     h = 448
#     lt = (center[0]-w//2,center[1]-h//3)
#     br = (lt[0]+w-1,lt[1]+h-1)
#     cv2.rectangle(img,lt,br,(0,0,255),3)


#     imgresize=cv2.resize(img,(1920//2,1280//2))
#     cv2.imshow('img',imgresize)
#     out_avi.write(imgresize)
#     cv2.waitKey(30)
# cap.release()
# out_avi.release()
