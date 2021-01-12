import open3d as o3d
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import sys
import json

NOT_PROCESSED_FILE_PATH = "./reduced_pc_1203_2.pcd"
PROCESSED_FILE_PATH = "./processed.pcd"
DISTANCE = 0.01

with open('./affine_parameter.json') as f:
    affine_parameter = json.load(f)

Px = affine_parameter['Px']
Py = affine_parameter['Py']
Pz = affine_parameter['Pz']
theta = affine_parameter['theta']
phi = affine_parameter['phi']

# 点群の読み込み
before_pcd = o3d.io.read_point_cloud(NOT_PROCESSED_FILE_PATH)
pc_arr = np.asarray(before_pcd.points)

# 回転行列の生成
y_matrix = np.matrix([[math.cos(-theta), 0, math.sin(-theta)],
                   [0, 1, 0], [-1 * math.sin(-theta), 0, math.cos(-theta)]])
z_matrix = np.matrix([[math.cos(-phi), -1*math.sin(-phi), 0],
                   [math.sin(-phi), math.cos(-phi), 0], [0, 0, 1]])
print('y_matrix:{}'.format(y_matrix))
print('z_matrix:{}'.format(z_matrix))

# 点群のアフィン変換
processed_arr = np.array([[0, 0, 0]])
for x, y, z in pc_arr:
    # 平行移動
    arr = np.array([[x-Px, y-Py, z-Pz]])
    # 回転移動
    arr = np.dot(arr, z_matrix.T)
    arr = np.dot(arr, y_matrix.T)
    # 回転後の点群配列の生成
    processed_arr = np.append(processed_arr, arr, axis=0)


processed_arr = np.delete(processed_arr, 0, 0)
t4 = time.time()


# 点群のpoint cloud オブジェクト化
after_pcd = o3d.geometry.PointCloud()
after_pcd.points = o3d.utility.Vector3dVector(processed_arr)
o3d.io.write_point_cloud(PROCESSED_FILE_PATH, after_pcd)


plane_model, inliers = after_pcd.segment_plane(distance_threshold=DISTANCE,
                                                ransac_n=3,
                                                num_iterations=1000)
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

# result_pcd = o3d.io.read_point_cloud(PROCESSED_FILE_PATH)
# o3d.visualization.draw_geometries([result_pcd, mesh_frame])
# print("平面抽出：{0}".format(t2-t1))
# print("アフィン変換：{0}".format(t4-t3))