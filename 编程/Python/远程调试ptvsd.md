## ptvsd+vscode
### 远程和桌面ptvsd安装
```python
pip install ptvsd
```

### 运行程序插入代码
```python
import ptvsd
ptvsd.enable_attach(address = ('172.17.13.13', 5678)) #Ip 为远程IP
ptvsd.wait_for_attach()
```

### vscode配置
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        
        
        {
            "type": "python",
            "request": "attach",
            "name": "Python Attach to Remote",
            "host": "172.17.xx.xx",
            "port": 5678,
            "pathMappings": [{
                "localRoot": "${workspaceFolder}",
                "remoteRoot": "/media/data2/xxx/project/python/tensorflow-DeepFM",
            }]
        },

        {
            "type": "python",
            "request": "launch",
            "name": "Python current file",
            "program": "${file}",
            "justMyCode": false
            //"console": "externalTerminal"
        }
    ]
}
```

### 运行
1. 先运行远程程序
2. 在本地切换到attach任务
3. F5即可停在断点出
   
## Pycharm
pycharm专业版本提供了远程调试的功能，[教程链接](https://www.cnblogs.com/xuegqcto/p/8621689.html)  
注意远程目录的映射  
设置debug运行脚本和参数传递：菜单Run->Configuration
![debug](pics/pycharm_remote_debug.png)

## PDB调试
利用python的pdb模块进行调试
[参考博客](https://www.cnblogs.com/xiaohai2003ly/p/8529472.html)
```
python -m pdb xxx.py
```