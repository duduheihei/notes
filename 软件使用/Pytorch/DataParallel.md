## 数据并行DataParallel
pytorch为了实现单机多卡并行训练方式，定义了torch.nn.DataParaller类，该类继承自Module，因此整个数据和模型的流程可以从该类入手查看

## DataParaller的初始化
初始化的内容十分简单，主要是获取gpu的id和个数，以及确定src_id,也就是host节点，后续需要将模型放在该节点上，才能进一步将模型“拷贝”至其他节点

## DataParaller的forward函数
### 数据分发scatter
该部分比较简单，直接看源码即可，采取递归方式，将输入inputs进行分发，如果是tensor则拷贝至目标设备，如果list,tuple,dicts数据结构则递归调用scatter函数，否则会拷贝引用

### 模型复制replicate
该部分也在forward函数中定义，意味着每次forward都需要重新进行拷贝  
首先利用Module函数的_replicate_for_data_parallel方法，生成一个新的model，新model将_parameters成员赋值为空，因为这里scatter操作使用了Broadcast类对模型进行了拷贝，拷贝过后参数由原先的Parameter类型变为普通的Tensor类型，因此也就不再是叶子节点，因此需要重新将拷贝的parameter设置为普通成员。具体地，Broadcast类继承自Function，因此具有apply方法，只需定义forward和backword函数，就可以将复制操作看作计算图的一部分，再做前向推理和反向传播。Broadcast再调用apply方法是，输入的是待复制的参数Parameter，返回的是各个devices上的Tensor，而不再是Parameter类型，具体apply是如何进行转换的，尚未了解清楚。得到复制的参数后，对各个device上复制的model进行子模块遍历，将子模块中的Parameter逐个替换为Tensor。

### parallel_apply
使用多线程，将每个模型和对应输入进行计算

### gather聚合结果
Gather也是继承自Function的一个类，在forward调用comm.gather用来合并结果，在backward类中调用了Scatter.apply用来分发梯度到每个模型  
这里要提一下Scatter类，该类与Gather类呈对称关系，其forward函数嗲用了comm.scatter用来分发，在backward函数中用了Gather操作去合并了梯度

### 反向传播与梯度更新
由于DataParallel类再复制model时将Parameter替换为Tensor，因此在调用model.parameters()方法时，只会获取到原始模型的参数，因此optimizer在更新梯度时也只会对这些参数进行更新
