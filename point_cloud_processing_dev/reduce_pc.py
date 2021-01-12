import open3d as o3d
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import sys

NOT_PROCESSED_FILE_PATH = "./pcd/pc_by_depth_05.pcd"

# 平面と点の距離閾値
DISTANCE = 0.01

# 点群のビジュアライズ
print("Load a ply point cloud, print it, and render it")
pcd = o3d.io.read_point_cloud(NOT_PROCESSED_FILE_PATH)
print(pcd)
# 軸オブジェクトの生成
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=1, origin=[0, 0, 0])
t1 = time.time()
voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.05)
t2 = time.time()
print(voxel_down_pcd)
# o3d.visualization.draw_geometries([pcd, mesh_frame])
# o3d.visualization.draw_geometries([voxel_down_pcd, mesh_frame])


def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

t3 = time.time()
cl, ind = voxel_down_pcd.remove_radius_outlier(nb_points=16, radius=0.15)
t4 = time.time()
o3d.visualization.draw_geometries([cl, mesh_frame])
display_inlier_outlier(voxel_down_pcd, ind)
o3d.io.write_point_cloud('./pcd/reduced_pc.pcd', cl)
print("ボクセルダウンサンプリング：{0}".format(t2 - t1))
print("外れ値除去：{0}".format(t4-t3))