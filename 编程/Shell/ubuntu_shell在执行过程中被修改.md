## shell脚本执行过程中发生了修改，会怎样？
[参考博客](https://bbs.csdn.net/topics/390481727?page=1)
当写好了process.sh文件，执行过程中修改了脚本文件，程序的运行结果会是怎么样？在ubuntu环境下测试结果如下：  
原脚本文件：  
```shell
python process1.py parm1 parm2 # 当前执行到该行

python process1.py parm3 parm4 

python process1.py parm5 parm6 
```
当解释器执行第一行命令时，修改shell文件为：
```shell
python process2.py parm1 parm2 # 当前行不被执行

python process2.py parm3 parm4 # 执修改后命令

python process2.py parm5 parm6 # 执修改后命令
```
脚本会从当前执行的位置后按照修改的脚本内容执行