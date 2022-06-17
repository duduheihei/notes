## RAFT: Recurrent All-Pairs Field Transforms for Optical Flow
文章为ECCV2020 best paper，在sintel-clean数据集上将光流预测的epe降低至1.609（flownet2为3.96）,将光流估计算法的表现提升了一个level。能达到这么好的效果，也是因为文章从网络架构上进行了改进，与U-NET网络结构不同的是，文章使用convGRU去refine光流，并且使用了双分支网络，一个分支用来计算特征相似性，一个分支用来提取context信息（光流结果与context具有关系）。为了减少计算量，每次前向仅计算一次特征相似性矩阵，后续需要使用时使用查找表的方式。由于网络使用了convGRU和特征相似矩阵计算，总体计算速度较慢，1088x436分辨率下，在1080Ti GPU上可以达到10fps，小网络版本可以达到20fps。

