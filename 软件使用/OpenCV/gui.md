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

## 直线/曲线绘制
[基于opencv的直线和曲线拟合与绘制（最小二乘法）](https://blog.csdn.net/guduruyu/article/details/72866144)
```c++
//绘制折线图
cv::Mat img_board = cv::Mat::zeros(480, 640, CV_8UC3);
img_board.setTo(cv::Scalar(100, 0, 0));
std::vector<cv::Point> points;
points.push_back(cv::Point(100., 58.));
points.push_back(cv::Point(150., 70.));
points.push_back(cv::Point(200., 90.));
points.push_back(cv::Point(252., 140.));
points.push_back(cv::Point(300., 220.));
points.push_back(cv::Point(350., 400.));
for (int i = 0; i < points.size(); i++)
{
    cv::circle(img_board, points[i], 5, cv::Scalar(0, 0, 255), 2, 8, 0);
}
cv::polylines(img_board, points, false, cv::Scalar(0, 255, 0), 1, 8, 0);
cv::imshow("img_board", img_board);
```