## Pandas

[知乎：pandas 在使用时语法感觉很乱，有什么学习的技巧吗？](https://www.zhihu.com/question/289788451/answer/1873472345)


### 获取size等信息
```python
df.info()
df.size #df文件所占内存大小
df.shape[0] #行数
df.shape[1] #列数
```

### 从列表新建DataFrame
```python
li = [
    [1, 2, 3, 4],
    [2, 3, 4, 5]
]

# DataFRame对象里面包含两个索引， 行索引(0轴， axis=0)， 列索引(1轴， axis=1)
d1 = pd.DataFrame(data=li, index=['A', 'B'], columns=['views', 'loves', 'comments', 'tranfers'])

```

### 行索引
```python
df.loc['indexKey']
# 索引最后一行
df.loc[df.shape[0]-1]
```

### 列索引
```python
df['columnKey']
# 索引最后一列
df.loc[:,df.shape[1]-1]
```

### 索引某行某列元素
```python
# 关键字索引
df.loc['indexKey','columnKey']
# 坐标索引
df.iloc[i,j]
```

### 删除行/删除列
注意如果需要就地删除，需要指定参数inplace=True
```python
#删除行
df.drop(['rowIndex0','rowIndex1'],axis=0)
# 删除列
df.drop(['columnKey0','columnKey1'],axis=1)
```

### 选取行/选取列
```python
# 选取行
df.loc[['rowIndex0','rowIndex1']]
# 选取列
df[['columnKey0','columnKey1']]
```

### 过滤行
```python
### 留下columnKey列值为1的行
df[df['columnKey']==1]

### 留下columnKey列值为[1,2,3,4]中的一个的行
df[df['columnKey'].isin([1,2,3,4])]

```

### 使用dataframe绘制折线图
```python
import matplotlib.pyplot as plt
columns = ['confLeftEyeClose','percloseLeftEye','confRightEyeClose','percloseRightEye']
dataFrames.loc['A'][columns].plot(subplots=True, sharex=True, figsize=(10,10))
plt.show()
```


### 保存DataFrame
```python
# -> Writes to a CSV file
df.to_csv(filename) 

# -> Writes to a CSV file
df.to_excel(filename) 

# -> Writes to a SQL table
df.to_sql(table_name, connection_object) 

# -> Writes to a file in JSON format
df.to_json(filename) 

# -> Saves as an HTML table
df.to_html(filename) 

# -> Writes to the clipboard
df.to_clipboard()

```

### 读取DataFrane
```python
# index_col指定index所在列
dataFrames = pd.read_csv(csv_file,index_col=[0])
```

### 修改列名  
```python
df.rename(columns = {'two':'new_name'},inplace=True)
```
### 拼接两个DataFrame (**concat、merge、join**)  
### 行拼接**concat**  
```python
df1=DataFrame(np.random.randn(3,4),columns=['a','b','c','d'])  
  
df2=DataFrame(np.random.randn(2,3),columns=['b','d','a'])  
  
pd.concat([df1,df2])  
  
          a         b         c         d  
0 -0.848557 -1.163877 -0.306148 -1.163944  
1  1.358759  1.159369 -0.532110  2.183934  
2  0.532117  0.788350  0.703752 -2.620643  
0 -0.316156 -0.707832       NaN -0.416589  
1  0.406830  1.345932       NaN -1.874817  
 
pd.concat([df1,df2],ignore_index=True)  
 
          a         b         c         d  
0 -0.848557 -1.163877 -0.306148 -1.163944  
1  1.358759  1.159369 -0.532110  2.183934  
2  0.532117  0.788350  0.703752 -2.620643  
3 -0.316156 -0.707832       NaN -0.416589  
4  0.406830  1.345932       NaN -1.874817

```

### 列拼接**merge**  
```python

import pandas as pd

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                       'A': ['A0', 'A1', 'A2', 'A3'],
                       'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']})
result = pd.merge(left, right, on='key',how='left)

# on参数传递的key作为连接键
result
Out[4]: 
    A   B key   C   D
0  A0  B0  K0  C0  D0
1  A1  B1  K1  C1  D1
2  A2  B2  K2  C2  D2
3  A3  B3  K3  C3  D3
————————————————


left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                      'key2': ['K0', 'K1', 'K0', 'K1'],
                         'A': ['A0', 'A1', 'A2', 'A3'],
                         'B': ['B0', 'B1', 'B2', 'B3']})

right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                      'key2': ['K0', 'K0', 'K0', 'K0'],
                         'C': ['C0', 'C1', 'C2', 'C3'],
                         'D': ['D0', 'D1', 'D2', 'D3']})

result = pd.merge(left, right, on=['key1', 'key2'])
# 同时传入两个Key，此时会进行以['key1','key2']列表的形式进行对应，left的keys列表是：[['K0', 'K0'],['K0', 'K1'],['K1', 'K0'],['K2', 'K1']],
left的keys列表是：[['K0', 'K0'],['K1', 'K0'],['K1', 'K0'],['K2', 'K0']]，因此会有1个['K0', 'K0']、2个['K1', 'K0']对应。

result
Out[6]: 
    A   B key1 key2   C   D
0  A0  B0   K0   K0  C0  D0
1  A2  B2   K1   K0  C1  D1
2  A2  B2   K1   K0  C2  D2

```


### 增加行
```python
df.loc['5']= [16,17,18,19]   # 后面的序列是Iterable就行
df.at['5']= [16,17,18,19]
df.set_value('5', df.columns, [16,17,18,19], takeable=False)   # warning，set_value会被取消
```

### 增加列
```python

df['columnKey']= 1

df['columnKey']= None
# 遍历赋值
for i in range(len(df)):
    df.iloc[i]['columnKey'] = 0
```

### split行/分割行
```python
df.iloc[i:j]
```


### 重新设置index索引
当对df进行操作时，如果选取一部分数据，或删除一部分数据后，得到一个新的df1，但是新df1的index仍然使用的原df的index，如果需要重新按照从0开始排序，可增加代码如下：
```python
df1.reset_index(drop=True, inplace=True)
```

### 获取每列的最大值/最小值
```python
df.max()
df.min()
```


### 获取每列的均值和方差
```python
df.mean()
df.var()
```

### 获取每列的和
```python
df.sum()
```

### 将多个Series合并为DataFrame
```python
s1 = pd.Series([1, 2], index=['A', 'B'], name='s1')
s2 = pd.Series([3, 4], index=['A', 'B'], name='s2')
pd.concat([s1, s2], axis=1)

#    s1  s2
# A   1   3
# B   2   4
```

### 排序
```python
# 按照reviewerID、unixReviewTime的顺序排列，reviewerID优先级高于unixReviewTime
sort_values(['reviewerID', 'unixReviewTime'])
```

### 获取列命
```python
print(df.columns.values)
```


### 转置
```python
df_t = df.T
```

### dataframe修改列名
```python
df.columns = ['columnName1','columnName2','columnName3',...]
```

### series修改索引名
```python
df.index = ['indexName1','indexName2','indexName3',...]
```

### 常用函数isna,isnull,fillna,unique,groupby,agg,sorted

### 常用属性columns,index,indices,size
