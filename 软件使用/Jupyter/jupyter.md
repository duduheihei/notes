## 安装
安装完anaconda后自带jupyter，可在命令行模式下使用```jupyter notebook```命令触发 

## 修改初始目录
jupyter初始目录是在home文件夹下，需要修改到自己指定的目录
```bat
jupyter notebook --generate-config
```
生成的配置文件在文件夹C:\Users\username\jupyter\jupyter_notebook_config.py下，打开后修改以下行
```python
## The directory to use for notebooks and kernels.
#c.NotebookApp.notebook_dir = ''
c.NotebookApp.notebook_dir = 'D:/project/notebooks'
```

## ubuntu上实现jupyter开启远程服务
[参考博客](https://blog.csdn.net/wl981292580/article/details/83659154)

