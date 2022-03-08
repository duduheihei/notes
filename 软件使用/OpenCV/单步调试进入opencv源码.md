## 使用debug版本库+对应pdb文件进行调试
[vs设置调试符号pdb](https://blog.csdn.net/mincheat/article/details/78644360)
1.找到opencv debug库对应的pdb文件所在文件夹，比如 D:\software\opencv\opencv3406\build\lib\Debug
2.找到testbed工程，工具->选项->调试->符号->浏览，将步骤1目录添加进去
3.设置断点并调试

## 使用opencv源工程进行调试
[让你的vs工程单步调试进入opencv源码](https://blog.csdn.net/huang826144283/article/details/54174268)
1.先新建好opencv工程，在debug模式下编译成功。
2.新建测试testbed，编译debug exe，testbed调用想调试的函数
3.打开opencv工程，将要调试的模块设置为启动项，并进入属性找到调试选项，填写步骤2的exe路径
4.在想调试的地方设置断点，F5

