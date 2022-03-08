## STGCN:  Spatial Temporal Graph Convolution Networks for Skeleton Based Action Recognition 
[论文解读](https://www.zhihu.com/search?type=content&q=STGCN)
[图卷积基础](https://www.zhihu.com/question/54504471/answer/611222866)
[mmaction2开源](https://github.com/open-mmlab/mmaction2/blob/master/configs/skeleton/stgcn/README.md)

### 三个邻接矩阵
首先了解center点的定义，一般指骨架点的重心，通常为neck点。  
作者依据当前点与关联点距离center的远近，将邻接矩阵分为三个，分别为距离更近、距离更远和距离相等。然后在使用图卷积计算特征时，对这三个邻接矩阵分配可学习的权重参数。  
ps为什么要将邻接矩阵分类？实际上该分类逻辑实际上是表达了不同尺度的特征