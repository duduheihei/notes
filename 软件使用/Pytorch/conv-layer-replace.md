## 简介
深度学习在使用预训练模型进行finetune时，很可能遇到输入通道数不一致的情况，比如预训练模型输入为RGB图像（3通道），而目标输入为灰度图（单通道）或者光流图（双通道），此时网络的第一层卷积层的输入通道不一致，因此需要修改。但是如果只是简单地使用一个随机参数的卷积层替换，那么该层预训练得到的先验信息将会丢失，因此一种常见的做法是把预训练的kernel在通道维度求平均，然后再扩充维度到目标维度，对新的卷积层参数进行替换，该方法在TSM网络的光流分支训练时得到使用。代码参考[TSM源码](https://github.com/mit-han-lab/temporal-shift-module/blob/master/ops/models.py#L305)

## 源码解读
代码很好理解，首先通过modules()方法找到第一个卷积层位置
```python
    def _construct_flow_model(self, base_model):
        # modify the convolution layers
        # Torch models are usually defined in a hierarchical way.
        # nn.modules.children() return all sub modules in a DFS manner
        modules = list(self.base_model.modules())
        # 获取第一个卷积层的索引
        first_conv_idx = list(filter(lambda x: isinstance(modules[x], nn.Conv2d), list(range(len(modules)))))[0]
        conv_layer = modules[first_conv_idx]
        container = modules[first_conv_idx - 1]

        # modify parameters, assume the first blob contains the convolution kernels
        # 通过parameters获得预训练参数weight,bias，如果卷积层设置bias=False，则只有weight
        params = [x.clone() for x in conv_layer.parameters()]
        kernel_size = params[0].size()
        # 这里kernel_size四个维度分别代表 c_out,c_in,k_h,k_w
        new_kernel_size = kernel_size[:1] + (2 * self.new_length, ) + kernel_size[2:]
        # 这里注意求均值使用了keepdim=True，这是为了方便后面expand函数的使用
        new_kernels = params[0].data.mean(dim=1, keepdim=True).expand(new_kernel_size).contiguous()

        new_conv = nn.Conv2d(2 * self.new_length, conv_layer.out_channels,
                             conv_layer.kernel_size, conv_layer.stride, conv_layer.padding,
                             bias=True if len(params) == 2 else False)
        # 替换卷积核
        new_conv.weight.data = new_kernels
        # 替换bias
        if len(params) == 2:
            new_conv.bias.data = params[1].data # add bias if neccessary
        # 通过state_dict().keys()方法获取属性名称并通过setattr完全替换卷积层
        layer_name = list(container.state_dict().keys())[0][:-7] # remove .weight suffix to get the layer name

        # replace the first convlution layer
        setattr(container, layer_name, new_conv)

        if self.base_model_name == 'BNInception':
            import torch.utils.model_zoo as model_zoo
            sd = model_zoo.load_url('https://www.dropbox.com/s/35ftw2t4mxxgjae/BNInceptionFlow-ef652051.pth.tar?dl=1')
            base_model.load_state_dict(sd)
            print('=> Loading pretrained Flow weight done...')
        else:
            print('#' * 30, 'Warning! No Flow pretrained model is found')
        return base_model
```