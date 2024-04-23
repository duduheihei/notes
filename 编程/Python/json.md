### 字典转字符串：
方法一： json.dumps() ,不管字典里是单引号还是双引号，都可以用json.dumps()转换成字符串，且转后都为双引号！ 
方法二： str()，用str将字典转成字符串后，双引号变成了单引号 
```python
with open(dstFile,'w') as f:
    json.dump(dicts,f,ensure_ascii=False) # ensure_ascii是为了防止中文乱码问题，该参数默认为True，会将中文编码转换为ascii格式
```


### 读取json字典
```python
with open(json_file,'r') as f:
    labels = json.load(f)

with open(json_file,'r') as f:
    for line in f.readlines():
        labels = json.loads(line)
```