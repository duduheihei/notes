## pytorch Hooks
[知乎介绍](https://zhuanlan.zhihu.com/p/276737137)  
[CSDN](https://blog.csdn.net/qq_45032341/article/details/105624136)  
pytorch为tensor和nn.module结构都提供了hook注册机制，能够在froward、backword前后插入一些操作，典型的应用包括：  
1. 通过打印模型信息调试程序
2. 对原模型进行包装，提取某些层的特征，得到一个输出特征的新模型
3. 梯度截断，只需要在backward后插入截断函数

1、torch.Tensor.register_hook(hook)  
2、torch.nn.Module.register_forward_hook  
3、torch.nn.Module.register_forward_pre_hook  
4、torch.nn.Module.register_backward_hook  

