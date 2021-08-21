如果网络中有部分模型无需计算梯度，那么可以用detach方法，该方法将 Variable 的grad_fn 设置为 None，因此BP不会再继续
