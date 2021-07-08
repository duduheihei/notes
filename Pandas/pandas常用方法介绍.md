## Pandas

[知乎：pandas 在使用时语法感觉很乱，有什么学习的技巧吗？](https://www.zhihu.com/question/289788451/answer/1873472345)


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
result = pd.merge(left, right, on='key')

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
