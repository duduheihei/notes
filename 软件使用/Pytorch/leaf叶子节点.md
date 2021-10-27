## torch.Tensor.is_leaf()
pytorch Tensor提供了is_leaf方法用来确认该Tensor是否为叶子节点，那么pytorch中叶子节点的定义是什么？  
[官方解释](https://pytorch.org/docs/stable/generated/torch.Tensor.is_leaf.html)  
1. 所有requires_grad = False 的tensor一定是叶子节点
2. requires_grad = True的tensor，但是是由用户创建，而非其他操作计算得到的，也为叶子节点，对应的grad_fn=None
3. 在调用backward()时，只有叶子节点的grad会更新，如果想获得非叶子节点的梯度，需要调用retain_grad()方法
