import pyrealsense2 as rs
import numpy as np
import cv2
import datetime
import os
import open3d as o3d
import time


align = rs.align(rs.stream.color)

# ストリーム(Color/Depth)の設定
config = rs.config()
config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 6)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

# get camera intrinsics
intr = profile.get_stream(
    rs.stream.color).as_video_stream_profile().get_intrinsics()
print(intr.width, intr.height, intr.fx, intr.fy, intr.ppx, intr.ppy)
pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
    intr.width, intr.height, intr.fx, intr.fy, intr.ppx, intr.ppy)

while True:
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)

    color_frame = aligned_frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())

    cv2.namedWindow('color image', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('color image', cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) != -1:
        print('finish')
        break

start = time.time()
depth_frame = aligned_frames.get_depth_frame()
depth = o3d.geometry.Image(np.asanyarray(depth_frame.get_data()))

pcd = o3d.geometry.PointCloud.create_from_depth_image(
    depth, pinhole_camera_intrinsic)
pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
elapsed_time = time.time() - start
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

pipeline.stop()
o3d.io.write_point_cloud('./pc_by_depth.pcd', pcd)
o3d.visualization.draw_geometries([pcd])
exit(0)
