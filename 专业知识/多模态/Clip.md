## CLIP : Contrastive Language-Image Pre-Training
[blog](https://openai.com/blog/clip/)
[paper](https://arxiv.org/pdf/2103.00020.pdf)

### 概述
原理简单且经典，联合图像和文本两个模态进行大规模（4亿图像,3w+句子)预训练。训练原理：利用文本-图像对，进行contrastive learning

### 缺点
1. 对于没有出现在预训练数据集中的类别表现不好
2. 对于一些逻辑问题表现不好，比如图片包含3个杯子
3. 对于细粒度的任务表现不好，比如区分车的细分车型、植物的细分类别

### 变种Clip4clip
 [github](https://github.com/ArrowLuo/CLIP4Clip)
 [知乎](https://zhuanlan.zhihu.com/p/443165620)
 利用预训练的clip模型，进行修改后用于视频检索任务。
