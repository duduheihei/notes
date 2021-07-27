## pathlib介绍
与os.path包类似 主要提供路径相关的操作，在较新的python版本才能使用，功能更加强大，接口更加简洁,并且自适应windows和linux系统

### 获取当前目录
```python
print(pathlib.Path.cwd())
```

### 获取当前文件路径
```python
print(__file__)
```

### 获取文件属性
```python
file = Path('archive/demo.txt')
print(file.stat())
print(file.stat().st_size)
print(file.stat().st_atime)
print(file.stat().st_ctime)
print(file.stat().st_mtime)
```

### name,stem,suffix,parent,anchor
.name 文件名，包含后缀名，如果是目录则获取目录名。
.stem 文件名，不包含后缀。
.suffix 后缀，比如 .txt, .png。
.parent 父级目录，相当于 cd ..
.anchor 锚，目录前面的部分 C:\ 或者 /。


### 遍历子路径
```
listdir
glob
rglob

```

### 删除文件
```
unlink
```

### 删除文件夹
```
rmdir
```

操作 | os and os.path | pathlib
---|----------------|--------
绝对路径 | os.path.abspath | Path.resolve
修改权限 | os.chmod | Path.chmod
创建目录 | os.mkdir | Path.mkdir
重命名 | os.rename | Path.rename
移动 | os.replace | Path.replace
删除目录 | os.rmdir | Path.rmdir
删除文件 | os.remove, os.unlink | Path.unlink
工作目录 | os.getcwd | Path.cwd
是否存在 | os.path.exists | Path.exists
用户目录 | os.path.expanduser | Path.expanduser and Path.home
是否为目录 | os.path.isdir | Path.is_dir
是否为文件 | os.path.isfile | Path.is_file
是否为连接 | os.path.islink | Path.is_symlink
文件属性 | os.stat | Path.stat, Path.owner, Path.group
是否为绝对路径 | os.path.isabs | PurePath.is_absolute
路径拼接 | os.path.join | PurePath.joinpath
文件名 | os.path.basename | PurePath.name
上级目录 | os.path.dirname | PurePath.parent
同名文件 | os.path.samefile | Path.samefile
后缀 | os.path.splitext | PurePath.suffix