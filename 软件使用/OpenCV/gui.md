## 根据视频位置，播放视频TrackBar
```python
capture = cv2.VideoCapture(videoName)
nFrames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
# capture.set(cv2.CAP_PROP_POS_FRAMES, nFrames)
# capture.read()
# duration = int(capture.get(cv2.CAP_PROP_POS_MSEC))
# print('nFrames',nFrames)
# pos = 0
# capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

def callback_Frame(x):
    capture.set(cv2.CAP_PROP_POS_FRAMES, x)
    print('here frame',x)

cv2.namedWindow('video')
cv2.createTrackbar('frame', 'video', 0, nFrames, callback_Frame)
cv2.setTrackbarPos('frame', 'video', 0)

while True:
    ret,img = capture.read()
    curPos = int(capture.get(cv2.CAP_PROP_POS_FRAMES))
    print('curPos ',curPos)
    cv2.setTrackbarPos('frame', 'video', curPos)
    cv2.imshow('video', img)
    if cv2.waitKey(30) == 113:
        break
```

