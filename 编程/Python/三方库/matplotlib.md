## 绘制折线图
```python
fig=plt.figure(figsize=(8, 4), dpi=300)
plt.xlabel('frame')
plt.ylabel('speed(m/s)')
plt.plot(speed_filter, lw=1, ls='-',marker="o",markersize=2)

with open(r'E:\database\optical_flow\adas\static\2points_0cm\speed.txt') as f:
    lines_single = f.readlines()
    speed_single = [float(line.strip()) for line in lines_single]

speed_single_filter = filter(speed_single)
plt.plot(speed_single_filter, lw=1, ls='-', marker="o",markersize=2)
#show出图形

with open(r'E:\database\optical_flow\adas\static\single_point\speed.txt') as f:
    lines_single = f.readlines()
    speed_single = [float(line.strip()) for line in lines_single]

speed_single_filter = filter(speed_single)
plt.plot(speed_single_filter, lw=1, ls='-', marker="o",markersize=2)
plt.legend(['0+45+100', 'single_point','8points'])
plt.show()
fig.savefig(r"E:\database\optical_flow\adas\static\2points40+100+140\speed_compare")
```