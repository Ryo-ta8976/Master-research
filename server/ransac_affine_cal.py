import open3d as o3d
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import sys
import json

NOT_PROCESSED_FILE_PATH = "./reduced_pc_1203_1.pcd"

# 平面と点の距離閾値
DISTANCE = 0.01

# 点群の平面抽出
before_pcd = o3d.io.read_point_cloud(NOT_PROCESSED_FILE_PATH)
plane_model, inliers = before_pcd.segment_plane(distance_threshold=DISTANCE,
                                                ransac_n=3,
                                                num_iterations=1000)
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

# 平面上の点Pの選択
out_arr = np.asarray(before_pcd.points)
for x, y, z in out_arr:
    if(abs(a*x+b*y+c*z+d)/math.sqrt(a*a+b*b+c*c) < DISTANCE):
        Py = y
        Pz = z
        break

Px = (-b*Py-c*Pz-d)/a
nx = a
ny = b
nz = c

# なす角の計算
theta = math.acos(nz/math.sqrt(nx*nx+ny*ny+nz*nz))
print('theta:{}'.format(theta))
if(ny >= 0):
    phi = math.acos(nx/math.sqrt(nx*nx+ny*ny))
else:
    phi = math.acos(nx / math.sqrt(nx * nx + ny * ny)) + math.pi

print('phi:{}'.format(phi))

with open('./affine_parameter.json', 'w') as f:
    dict_param = {'theta': theta, 'phi': phi, 'Px': Px, 'Py': Py, 'Pz': Pz}
    json.dump(dict_param, f, indent=4)