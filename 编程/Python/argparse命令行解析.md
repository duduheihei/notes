## argparse
### 初级使用
```python
parser = argparse.ArgumentParser()
parser.add_argument('--target',type=int,default=0,help="0: camera, 1: single video , 2: multi-processes for videos ")
parser.add_argument('--file',type=str,default=None,help="Needed in video mode, specify file need to be processed")
args = parser.parse_args()
```

### 采坑
当需要输入一个bool值做参数是，不能通过输入True或者False作为选择，因为对一个字符串进行强制转换，无论输入任何值，都会被转义为True。此时应该使用
