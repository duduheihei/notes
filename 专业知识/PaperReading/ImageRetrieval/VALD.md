# VLAD
[知乎参考链接](https://zhuanlan.zhihu.com/p/96718053)  

## 简介
该方法是图像检索领域常用的一种方法，用于提取图像的特征，其首先提取出图像的N个维度为D的特征向量（SIFT、SURF），然后进行聚类得到K个D维的中心向量，然后在每个中心向量附近计算从属于该类的特征残差值之和，最终得到K个维度为D的特征，即为图的全局特征。该特征抹去了图像本身的特征分布差异，只保留了局部特征与聚类中心分布的差异  

# NetVLAD
[pytorch实现](https://github.com/lyakaap/NetVLAD-pytorch)  
经典的VLAD特征计算不可导，因此需要进行修改，将其变得可导，因此得到一个可训练的VLAD模块，成为NetVLAD