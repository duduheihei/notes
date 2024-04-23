## 利用RANSAC进行FOE估计
```python

def cal_foe(points_t0,points_t1):
    '''
    points_t0:关键点在前一帧图像的坐标，(n*2)
    points_t1:关键点在后一帧图像的坐标, (n*2)
    '''
    # 手动取三个点进行验证
    # points_t0 = np.zeros((3,2))
    # points_t0[0,0] = 480
    # points_t0[0,1] = 480
    # points_t0[1,0] = 240
    # points_t0[1,1] = 720
    # points_t0[2,0] = 720
    # points_t0[2,1] = 720
    # points_t1 = np.zeros((3,2))
    # points_t1[0,0] = 480
    # points_t1[0,1] = 960
    # points_t1[1,0] = 0
    # points_t1[1,1] = 960
    # points_t1[2,0] = 960
    # points_t1[2,1] = 960
    
    # points_t1 = points_t1[points_t0[:,0]>=240]
    # points_t0 = points_t0[points_t0[:,0]>=240]
    # points_t1 = points_t1[points_t0[:,0]<=720]
    # points_t0 = points_t0[points_t0[:,0]<=720]
    # points_t1 = points_t1[points_t0[:,1]>=320]
    # points_t0 = points_t0[points_t0[:,1]>=320]
    # points_t1 = points_t1[points_t0[:,1]<=960]
    # points_t0 = points_t0[points_t0[:,1]<=960]
    # 过滤掉光流过短的点，过短的点会带来较大的噪声
    # flow=points_t1-points_t0
    # ind = flow[:,0]*flow[:,0]+flow[:,1]*flow[:,1]>5*5
    # points_t0 = points_t0[ind]
    # points_t1 = points_t1[ind]
    # if len(points_t0)<20:
    #     return np.array([0,0])


    flow=points_t1-points_t0
    A = flow[:,::-1]
    A[:,1] = -A[:,1]
    b = A[:,0]*points_t0[:,0]+A[:,1]*points_t0[:,1]
    matrix = np.matmul(A.T,A)
    u, s, v = np.linalg.svd(matrix, full_matrices=False)
    inv = np.matmul(v.T * 1 / s, u.T)
    foe = np.matmul(inv,np.matmul(A.T,b))
    return foe

def ransacFOE(points_t0,points_t1,n,percent=0.2):
    count = 0
    optimal_center = None
    sample_cnt = int(len(points_t0)*percent)
    flow = points_t1-points_t0
    k = flow[:,1]/flow[:,0]
    for i in range(n):
        pair = list(zip(points_t0,points_t1))
        pair = random.sample(pair,sample_cnt)
        points0,points1 = zip(*pair)
        points0 = np.array(points0)
        points1 = np.array(points1)
        center = cal_foe(points0,points1)
        dis = (k*center[0]-center[1]+points_t0[:,1]-k*points_t0[:,0])/np.sqrt(1+k*k)
        if np.sum(dis<10)>count:
            count = count
            optimal_center = center
        print('total inner points: {} percent: {}'.format(np.sum(dis<5),np.sum(dis<5)/len(points_t0)))
    return optimal_center

```