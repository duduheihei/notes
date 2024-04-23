## pybind11
[github](https://github.com/pybind/pybind11)  
[docs](https://pybind11.readthedocs.io/en/stable/basics.html)

### 简介
在工程中，通常使用c/c++等语言编写库，但是有时需要使用python调用这些库，但是如何实现呢？pybing11便是一种“head-only”式的轻量级框架，只需要在c/c++语言中加入一些代码，便可以得到可供python导入的库。

### windows安装
python版本：3.7  
pybind11版本：2.7.1  
visual studio版本：vs2019 x64  
通过pip在miniconda虚拟环境中安装pybind11:
```bat
pip install pybind11
```

&nbsp;
### 工程配置
在vs工程中，需要将pybind11的include文件夹设为可包含目录，python的include目录设为可包含目录，以及python3.lib和python37.lib两个库的链接位置，这里使用cmakelist文件设置：
```shell

list(APPEND LINKER_LIBS C:/Users/xxx/AppData/Local/Continuum/anaconda3/envs/torch16/libs/python3.lib)
list(APPEND LINKER_LIBS C:/Users/xxx/AppData/Local/Continuum/anaconda3/envs/torch16/libs/python37.lib)

target_include_directories(testbed PRIVATE C:/Users/xxx/AppData/Local/Continuum/anaconda3/envs/torch16/include)
target_include_directories(testbed PRIVATE C:/Users/xxx/AppData/Local/Continuum/anaconda3/envs/torch16/Lib/site-packages/pybind11/include)

```
另外需要在项目属性中，修改输出文件的后缀为“.pyd”，类型为“dll”：属性-->配置属性-->高级-->高级属性-->目标文件扩展名

### 简单例子
```cpp
#include<pybind11/pybind11.h>

namespace py = pybind11;
int add(int i, int j) {
	return i + j;
}
PYBIND11_MODULE(testbed, m) {
	m.doc() = "pybind11 example plugin"; // optional module docstring

	m.def("add", &add, "A function which adds two numbers");
}
```
这里PYBIND11_MODULE中第一个参数，必须与导出库文件的文件名一致，这里生成文件必须名为“testbed.pyd”。然后便可以在python代码中进行调用：
```python
import sys
sys.path.append(r'd:/') #添加库所在路径
import testbed
out = testbed.add(1,2)
print(out)
```

### pybind导出类
[参考博客](https://blog.csdn.net/weixin_41045354/article/details/109159065)

### 输入参数是结构体
[参考博客](https://www.jb51.net/article/181254.htm)

### 输入参数是指针
[参考博客](https://blog.csdn.net/tcy23456/article/details/117659776)  
当参数类型是指针时，需要使用到py::buffer, 当输入参数时numpy array时，需要使用py::array_t<T>，此时需要包含numpy.h头文件  
```c++
// 将python的numpy输入转化为mat
cv::Mat numpy_uint8_1c_to_cv_mat(py::array_t<unsigned char>& input) {
	if (input.ndim() != 2) throw std::runtime_error("1-channel image must be 2 dims ");
	py::buffer_info buf = input.request();
	cv::Mat mat(buf.shape[0], buf.shape[1], CV_8UC1, (unsigned char*)buf.ptr);
	return mat;
}

cv::Mat numpy_uint8_3c_to_cv_mat(py::array_t<unsigned char>& input) {
	if (input.ndim() != 3) throw std::runtime_error("3-channel image must be 3 dims ");
	py::buffer_info buf = input.request();
	cv::Mat mat(buf.shape[0], buf.shape[1], CV_8UC3, (unsigned char*)buf.ptr);
	return mat;
}
```

### 采坑：ImportError: DLL load failed: 找不到指定的模块
当编译得到.pyd文件后，将.pyd文件拷贝至待运行py文件同级目录下，然后使用import语句导入模块，在vscode选择对应anaconda虚拟环境，然后执行成功导入模块并验证结果。但是使用anaconda prompt命令行模式执行py文件时，报错“ImportError: DLL load failed: 找不到指定的模块”。一开始查找资料表明可能是python版本与编译时的版本不一致，或者vs编译设置存在问题。但是注意.pyd确实已经可以成功导入了，说明不是这些问题。考虑到编译目标时是存在dll动态库依赖的，因此可能在anaconda环境下无法找到依赖的dll，因此将依赖dll同样拷贝至.pyd同级目录，然后导入成功！


## Linux/Ubuntu 安装
```bash
# pip安装
pip install pybind11
```
```bash
# 编译
conda activate torch
git clone xxx
cd xxx
mkdir build && cd build
# 指定安装路径和python环境
cmake -DDOWNLOAD_EIGEN=ON -DCMAKE_INSTALL_PREFIX=install ..
make check -j 4
make  -j 8
make install
```

## cmake命令
```cmake
set(TARGET_NAME packet)
set(pybind11_DIR "/media/data2/bqj/software/pybind11/build/install/share/cmake/pybind11" CACHE PATH "pybind11 DIR")
find_package(pybind11 CONFIG)
MESSAGE( [MAIN] "Found pybind11 v${pybind11_VERSION}: ${pybind11_INCLUDE_DIRS}")
MESSAGE( [Main] " pybind11_INCLUDE_DIRS = ${pybind11_INCLUDE_DIRS}")
MESSAGE( [Main] " pybind11_LIBRARIES = ${pybind11_LIBRARIES}")
pybind11_add_module(${TARGET_NAME} ${TESTBED_SRCS})
target_link_libraries(${TARGET_NAME} PUBLIC  pybind11::module ${TESTBED_LINKER_LIBS} ${pybind11_LIBRARIES}  facial_action_recognition)
```


### 采坑
1. 编译时报错“can not be used when making a shared object; recompile with -fPIC”，此时按照提示应该在cmake中增加编译选项，使用```set(CMAKE_CXX_FLAGS "-fPIC")```设置发现无法解决，后来换成```add_compile_options("-fPIC")```编译成功，原因是```add_compile_options``命令添加的编译选项是针对所有编译器的(包括c和c++编译器)，而set命令设置```CMAKE_C_FLAGS或CMAKE_CXX_FLAGS```变量则是分别只针对c和c++编译器的。[参考链接](https://blog.csdn.net/10km/article/details/51731959)
2. ubuntu当目标库存在依赖库时，[cmake应该如何写](https://github.com/pybind/pybind11/issues/1527)
3. [cmake的官方教程](https://pybind11.readthedocs.io/en/stable/cmake/index.html)
4. 在使用宏控制c++文件中的pybind相关代码时不要使用`PYBIND`，该宏在使用其他库时可能被定义，导致自己的代码宏实现，使用`ARC_PYBIND`替代
5. 在cmake切换option的时候，需要删除编译目录即中间缓存文件，重新编译

## 后期工作
有时候需要将多个cpp中的接口打包到一个包中，但是c++后的PYBIND11_MODULE无法在两个cpp文件中传入相同的模块名，如何进行实现以后会进一步探讨




