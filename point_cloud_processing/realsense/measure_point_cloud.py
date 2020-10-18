import pyrealsense2 as rs
import numpy as np
import cv2
import datetime
import os
import open3d as o3d

align = rs.align(rs.stream.color)

# ストリーム(Color/Depth)の設定
config = rs.config()
config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 6)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)


# # 距離の計算 距離[m] = depth * depth_scale
# depth_sensor = profile.get_device().first_depth_sensor()
# depth_scale = depth_sensor.get_depth_scale()

# # レーザー出力の設定(0~100)
# set_laser = 100
# depth_sensor.set_option(rs.option.laser_power, set_laser)
# # レーザー出力の確認
# laser_pwr = depth_sensor.get_option(rs.option.laser_power)
# print("laser power = ", laser_pwr)

# # 抽出範囲（meter）
# clipping_distance_in_meters_min = 0.11  # meter
# clipping_distance_in_meters_max = 0.65  # meter

# clipping_distance_min = clipping_distance_in_meters_min / depth_scale
# clipping_distance_max = clipping_distance_in_meters_max / depth_scale


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

depth_frame = aligned_frames.get_depth_frame()


# depth_image = np.asanyarray(depth_frame.get_data())
# depth_image_3d = np.dstack((depth_image, depth_image, depth_image))
# depth_color_image = np.asanyarray(color_frame.get_data())
# bg_removed = np.where((depth_image_3d > clipping_distance_min) & (
#     depth_image_3d < clipping_distance_max), depth_color_image, 0)
# bg_removed_uint8 = np.asanyarray(bg_removed, dtype=np.uint8)


# depth = o3d.geometry.Image(bg_removed_uint8)
depth = o3d.geometry.Image(np.asanyarray(depth_frame.get_data()))
color = o3d.geometry.Image(color_image)

rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
    color, depth, convert_rgb_to_intensity=False)
pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
    rgbd, pinhole_camera_intrinsic)
pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

pipeline.stop()
o3d.io.write_point_cloud('./pc_color.pcd', pcd)
o3d.visualization.draw_geometries([pcd])
