## 绘制混淆矩阵
```python
import pandas as pd 
print(label2action.keys())
keys = [chinese2english[label2action[key]] for key in label2action.keys()]
df = pd.DataFrame(matrix,columns=keys,index=keys).astype('int')

import seaborn as sns
import matplotlib.pyplot as plt
sns.heatmap(df,annot=True,fmt='d') #这里fmt设置矩阵内容的输出格式，'d'表示输出整型
plt.show()
```

## 绘制箱形图、柱状图、饼图
[参考](https://www.kaggle.com/sergiogaleano/airbnb-2019-nyc-dataset-tutorial#4.-Explore-&-Visualize-the-Data)




