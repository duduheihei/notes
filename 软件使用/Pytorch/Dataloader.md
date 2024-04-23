## Dataloader
pytorch自带的数据迭代器，在使用时有两个参数需要注意，一个是num_workers，另一个是prefetch_factor  
num_workers：多线程处理，每个线程会使用batch_sampler读取batch_size个数据，然后n个线程会将n个batch数据送入queue中，设置过大会消耗内存，适合预处理计算量大的任务  
[参考](https://blog.csdn.net/qq_24407657/article/details/103992170)  
prefetch_factor：预取参数，通常设置为2，那么每个worker就会读取2个batch，如果IO比较慢，可以设置为2或者2以上  
[参考](https://github.com/pytorch/pytorch/issues/58030)  
pin_memory: 设置为True后，dataloader会将tensor拷贝到cuda的pin memory上，GPU知道页锁定内存的物理地址，可以通过“直接内存访问（Direct Memory Access，DMA）”技术直接在主机和GPU之间复制数据，速率更快。由于每个页锁定内存都需要分配物理内存，并且这些内存不能交换到磁盘上，所以页锁定内存比使用标准malloc()分配的可分页内存更消耗内存空间。  
[CUDA页锁定内存（Pinned Memory）](https://blog.csdn.net/dcrmg/article/details/54975432)