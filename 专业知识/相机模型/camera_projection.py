import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

#参考博客 https://blog.csdn.net/weixin_41010198/article/details/115960331
# https://blog.csdn.net/weixin_46534973/article/details/127538686

def eulerAnglesToRotationMatrix(theta):
    # pitch
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(theta[0]), -np.sin(theta[0])],
                    [0, np.sin(theta[0]), np.cos(theta[0])]
                    ])
    # yaw
    R_y = np.array([[np.cos(theta[1]), 0, np.sin(theta[1])],
                    [0, 1, 0],
                    [-np.sin(theta[1]), 0, np.cos(theta[1])]
                    ])
    # roll
    R_z = np.array([[np.cos(theta[2]), -np.sin(theta[2]), 0],
                    [np.sin(theta[2]), np.cos(theta[2]), 0],
                    [0, 0, 1]
                    ])

    R = np.dot(R_z, np.dot(R_y, R_x))
    print(f"Rotate matrix:\n{R}")
    return R


# pitch = -0.269127*math.pi/180+2.*math.pi/180
pitch = -0.269127*math.pi/180
yaw = 1.130816*math.pi/180
roll = -0.371539*math.pi/180
thetas = [pitch,yaw,roll]

# Cameras intrinsic parameters [K] (f~420px, w~710px, h~500px)
K = np.array(
    [[1161.588, 0.,          970.939],
     [0.,         1164.719,  635.581],
     [0.,         0.,          1.]]
)

# Relative camera position [R|t] in respect wo world coordinate system
# Rotatio matrix in radian
# R = np.array(
#     [[0.9972,   -0.0699,  0.0263],
#      [0.0553,    0.9299,  0.3598],
#      [-0.0501,  -0.3572,  0.9312]]
# )
R = eulerAnglesToRotationMatrix(thetas)

# Translation vector in meters
# t = np.array(
#     [[-0.1070],
#      [-0.1471],
#      [0.3985 ]]
# )
t = np.array(
    [[2.429],
     [-2.54],
     [1.500]]
)


T = np.concatenate((R, t), axis=1)

#单位是米
Pw = np.array(
    [[20], # lateral distance
     [0], # height
     [40], # long distance
     [1]]
)

Pc = np.matmul(T, Pw)
p = np.matmul(K, Pc)
uv = (p / p[2][0])[:-1]
print(uv)

Pw = np.array(
    [[10], # lateral distance
     [2], # height
     [40], # long distance
     [1]]
)

Pc = np.matmul(T, Pw)
p = np.matmul(K, Pc)
uv = (p / p[2][0])[:-1]
print(uv)


