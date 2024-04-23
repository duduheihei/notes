## [官方编译教程](https://github.com/Tencent/ncnn/wiki/how-to-build#build-for-windows-x64-using-visual-studio-community-2017)
1.使用visual studio自带的命令行工具
Start → Programs → Visual Studio 2017 → Visual Studio Tools → x64 Native Tools Command Prompt for VS 2017

2.下载[protobuf](https://github.com/google/protobuf/archive/v3.4.0.zip),并解压

3.安装protobuf，如果需要单步调试ncnn，这里需要将cmake参数设置为Debug
```shell
cd <protobuf-root-dir>
mkdir build
cd build
cmake -G"NMake Makefiles" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=%cd%/install -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_MSVC_STATIC_RUNTIME=OFF ../cmake
nmake
nmake install
```

4.编译安装ncnn,同样需要将编译选项改为Debug，关闭NCNN_VULKAN，
```shell
cd <ncnn-root-dir>
mkdir build
cd build
cmake -G"NMake Makefiles" -DOpenCV_DIR=D:/software/opencv/opencv3406/buildx86/install -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=%cd%/install -DProtobuf_INCLUDE_DIR=d:/software/protobuf/protobuf-3.4.0/build_dir/install/include -DProtobuf_LIBRARIES=d:/software/protobuf/protobuf-3.4.0/build_dir/install/lib/libprotobuf.lib -DProtobuf_PROTOC_EXECUTABLE=d:/software/protobuf/protobuf-3.4.0/build_dir/install/bin/protoc.exe -DNCNN_VULKAN=OFF ..
nmake
nmake install
```

5.使用ncnn.pdb进行单步调试，只有debug编译才会生成该文件，文件位于build\src\CMakeFiles\ncnn.dir\ncnn.pdb