[参考](https://blog.csdn.net/ysngki/article/details/114983706)
## 1. NLLLose与Cross Entropy
他们的输入是（概率，标签）这样的二元组。
一个例子：假设三分类任务最后的输出是这三个数 [0.8, 0.2, 0.7]。标签是0。
想要用cross entropy计算损失，那么我们直接把这两个丢进去就好了，不用做任何处理，loss = cross_entropy( probability, label )。
想要丢到NLLLose函数中计算损失的话，我们首先要对 [0.8, 0.2, 0.7] 计算softmax，假设结果是 [0.45, 0, 0.40, 0.15]， 然后再求个对他的每个概率求个log，然后把处理后的概率丢到函数里，计算 loss = NLLLose( probability, label ）。

## 2. MSE与KLDivLoss
他们的输入是一串向量，label也是一串向量，所以可以用来衡量两串向量间的接近程度。

经过数学证明，KLDiv是恒大于0的，可以放心使用。至于它和MSE之间的效果区别，笔者目前未知，大家可留言分享。

KLDiv还会用在label smoothing中。

