import numpy as np
import cv2
import datetime
import os
import open3d as o3d
import time
import csv
import re

width = 1280
height = 720
fx = 906.9666137695312
fy = 907.3667602539062
ppx = 642.673828125
ppy = 376.1431579589844
# get camera intrinsics
pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
    width, height, fx, fy, ppx, ppy)


start = time.time()
with open('./pcd/temp_point_cloud/depth.csv') as f:
    reader = csv.reader(f)
    depth_image = [row for row in reader]

with open('./pcd/temp_point_cloud/color.csv') as f:
    reader = csv.reader(f)
    color_image = [[re.findall(r'\d+', array) for array in row] for row in reader]
    # color_image = [[array.replace(' ', ',') for array in row] for row in reader]

# depth_frame = aligned_frames.get_depth_frame()
print(color_image)
print(type(np.asanyarray(color_image, dtype='uint16')))
depth = o3d.geometry.Image(np.asanyarray(depth_image, dtype='uint16'))
color = o3d.geometry.Image(np.asanyarray(color_image, dtype='uint16'))

# depth & color to pcd
# rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
#     color, depth, convert_rgb_to_intensity=False, depth_trunc=20.0)
# pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
#     rgbd, pinhole_camera_intrinsic)

# depth to pcd
pcd = o3d.geometry.PointCloud.create_from_depth_image(
    depth, pinhole_camera_intrinsic)
pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

elapsed_time = time.time() - start
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

o3d.io.write_point_cloud('./pcd/pc_by_rgbd.pcd', pcd)
o3d.visualization.draw_geometries([pcd])
exit(0)
