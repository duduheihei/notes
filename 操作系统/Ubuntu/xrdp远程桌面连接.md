[xrdp远程桌面连接](https://www.jianshu.com/p/9dbe0176426f)
[参考2](https://www.linuxidc.com/Linux/2017-09/147112.htm)
[xrdp tab补全](https://blog.csdn.net/ybw123w/article/details/89162156)
注意，在设置快捷时不要用sudo权限

## ubuntu18.04
[一键安装](https://blog.csdn.net/weixin_43315707/article/details/107518380)

### 安装
```shell
#安装xrdp 
sudo apt-get install xrdp 
#安装vnc4server 
sudo apt-get install vnc4server tightvncserver
#安装xubuntu-desktop 
sudo apt-get install xubuntu-desktop 
#向xsession中写入xfce4-session 
echo “xfce4-session” > ~/.xsession 
#开启xrdp服务 
sudo service xrdp restart

# 在执行上述步骤之后，出现使用远程桌面连接ubuntu服务器时出现连接成功后闪退的情况，后来尝试了好多其他安装方法，依然存在此问题，后来找到了解决方法：
sudo apt-get install xfce4
touch ~/.session
sudo vim /etc/xrdp/startwm.sh     # 在. /etc/X11/Xsession前面加xfce4-session
sudo service xrdp restart         # 重启服务
```

### 设置Tab 补全
1.在终端中输入xfwm4-settings打开（xfwm4就是xfce4 window manger的缩写）
```
xfwm4-settings
```
2.在出现的windows manager中选择keyboard，将与Tab键选项相关的快捷键清除后关闭窗口即可。
