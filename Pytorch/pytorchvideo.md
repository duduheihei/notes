# PytorchVideo
[官方教程](https://pytorchvideo.org/docs/tutorial_overview)
[源码链接](https://github.com/facebookresearch/pytorchvideo)

## 简介
针对视频网络计算量大，deploy困难的问题，对一些经典网络模块3DResBlock，3Dconv等使用2Dconv进行了等价替换，并进行了封装模块化，以提升速度，并且对于后量化将fuse操作包含在了预定义的网络中