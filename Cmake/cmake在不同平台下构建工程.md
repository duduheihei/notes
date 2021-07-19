## Vs2019 x64
```bat
@echo off

set BUILD_DIR=vs2019-x64
if not exist %BUILD_DIR% md %BUILD_DIR%
cd %BUILD_DIR%
cmake ../.. -G "Visual Studio 16 2019" -A x64
cd ..
pause
```

## vs2019 x86
```bat
@echo off

set BUILD_DIR=vs2019-x86
if not exist %BUILD_DIR% md %BUILD_DIR%
cd %BUILD_DIR%
cmake ../.. -G "Visual Studio 16 2019" -A Win32
cd ..
pause
```

## 在cmakelist文件中如何判断x86和x64
```cmake
	IF(CMAKE_CL_64)
		  set(OpenCV_DIR "D:/software/opencv/opencv3406/build/install" CACHE PATH "OPENCV DIR")
	ELSE(CMAKE_CL_64)
		  set(OpenCV_DIR "D:/software/opencv/opencv3406/buildx86/install" CACHE PATH "OPENCV DIR")
	ENDIF(CMAKE_CL_64)
```

## linux工程构建
```bash
export BUILD_DIR=linux-x64
if [ ! -d $BUILD_DIR ];then
   mkdir -p $BUILD_DIR
fi
cd $BUILD_DIR

cmake ../.. 
make -j4

cd ..
```

## android工程
```bat
@echo off


set TOOLCHAIN=D:/software/android-ndk-r21b/build/cmake/android.toolchain.cmake

echo "ANDROID_NDK is %ANDROID_NDK%"
echo "TOOLCHAIN is: %TOOLCHAIN%"

set BUILD_DIR=android-arm64
if not exist %BUILD_DIR% md %BUILD_DIR%
cd %BUILD_DIR%

cmake -G Ninja ^
    -DCMAKE_TOOLCHAIN_FILE=%TOOLCHAIN% ^
    -DANDROID_ABI="arm64-v8a" ^
    -DANDROID_PLATFORM=android-24 ^
    -DCMAKE_BUILD_TYPE=Release ^
    ../..

ninja

cd ..
```

