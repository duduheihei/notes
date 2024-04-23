## FCOS: Fully Convolutional One Stage Object Detection
[FCOS论文精读](https://zhuanlan.zhihu.com/p/339023466)
[FCOS 的改进 trick](https://zhuanlan.zhihu.com/p/259314634)
关键点：
1）正样本选取，gt框内的点，为正样本
2）直接回归点到上下左右四条边的距离，由于是非负值，因此会在输出加上exp操作
3）每一层level对应不同大小的box，如果gt的四个距离超出限制，则认为是负样本，这样可以解决像素点目标重叠问题，无法确定对应哪个目标框，让不同的feature检测不同大小的物体，即使这些物体存在重叠。
4) 通过IOU计算每个点的centerness进行回归

