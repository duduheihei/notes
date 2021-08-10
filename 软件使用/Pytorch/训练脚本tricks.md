### 保存模型定义py文件
在使用pytorch获取```model```之后，可以通过python的inspect模块获取model class instance对应的class定义所在py文件路径
```python
def get_model_path(model):
    assert isinstance(model, nn.Module)
    return inspect.getfile(model.__class__)
```

