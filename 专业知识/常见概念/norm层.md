## 深度学习常见norm层
输入维度N,C,H,W
1. **batch norm**: 对N,H,W维度求均值方差，参数维度为C*4
2. **layer norm**: 主要对rnn作用明显，RNN同一个batch中输入的数据长短不一，不同的时态下需要保存不同的统计量，无法正确使用BN层，只能使用Layer Normalization。对C,H,W维度求均值方差，LayerNorm中不会像BatchNorm那样跟踪统计全局的均值方差，因此train()和eval()对LayerNorm没有影响。如果elementwise_affine设置为True,会对归一化后的值做仿射变换，此时才会有参数，并且参数维度为LayerNorm的输入normalized_shape*2
   [pytorch LayerNorm详解](https://blog.csdn.net/weixin_39228381/article/details/107939602)
3. **InstanceNorm**： 主要对风格迁移作用明显，一个channel内做归一化，算H*W的均值，用在风格化迁移；因为在图像风格化中，生成结果主要依赖于某个图像实例，所以对整个batch归一化不适合图像风格化中，因而对HW做归一化。可以加速模型收敛，并且保持每个图像实例之间的独立。
 [torch文档解释](https://pytorch.org/docs/stable/generated/torch.nn.InstanceNorm2d.html)：
 InstanceNorm2d and LayerNorm are very similar, but have some subtle differences. InstanceNorm2d is applied on each channel of channeled data like RGB images, but LayerNorm is usually applied on entire sample and often in NLP tasks. Additionally, LayerNorm applies elementwise affine transform, while InstanceNorm2d usually don’t apply affine transform.
4. **group norm**：将channel方向分group，然后每个group内做归一化，算(C//G)HW的均值；这样与batchsize无关,$torch.nn.GroupNorm$