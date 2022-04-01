[cuda编程常见概念介绍](https://developer.nvidia.com/blog/even-easier-introduction-cuda/)
[pytorch教程](https://pytorch.org/tutorials/advanced/cpp_extension.html#motivation-and-example)

## cuda关键词
__global__：告诉编译器这是在gpu上运行的函数

## 内存分配
```c
// Allocate Unified Memory -- accessible from CPU or GPU
float *x, *y;
cudaMallocManaged(&x, N*sizeof(float));
cudaMallocManaged(&y, N*sizeof(float));
// Free memory
cudaFree(x);
cudaFree(y);
```

## 同步
```c
// 所有并行计算完成后再执行下一步
cudaDeviceSynchronize()
```

## nvprof查看函数耗时
```shell
nvprof ./add_cuda
```

## block, threads
cuda再并行计算时，会将线程划分为若干个block，每个block包含32*n个threads。比如
```c
// 10个block,每个block256个threads
add<<<10，256>>>(N, x, y);

// 长度为N的数组进行并行计算
__global__
void add(int n, float *x, float *y)
{
  int index = threadIdx.x;
  int stride = blockDim.x;
  for (int i = index; i < n; i += stride)
      y[i] = x[i] + y[i];
}
```

## CUDA软件架构—网格（Grid）、线程块（Block）和线程（Thread）的组织关系以及线程索引的计算公式
[参考](https://www.cnblogs.com/dama116/p/6909629.html)
[参考](https://blog.csdn.net/dcrmg/article/details/54867507?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_aa&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_aa&utm_relevant_index=1)

