import pyrealsense2 as rs
import numpy as np
import datetime
import os
import time
import csv
import log

align = rs.align(rs.stream.color)

# ストリーム(Color/Depth)の設定
config = rs.config()
config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

print('measure point cloud')
log.log('measure point cloud')
start = time.time()
frames = pipeline.wait_for_frames()
aligned_frames = align.process(frames)
depth_frame = aligned_frames.get_depth_frame()
depth_image = np.asanyarray(depth_frame.get_data())
color_frame = aligned_frames.get_color_frame()
color_image = np.asanyarray(color_frame.get_data())

pipeline.stop()

def ndarray_to_csv(file_name, ndarray):
  with open(file_name, 'w') as f:
    writer = csv.writer(f)
    for value in ndarray:
      writer.writerow(value)
    # list(map(lambda x: writer.writerow(x), ndarray))

print('change depth array to csv')
log.log('change depth array to csv')
ndarray_to_csv('./temp_point_cloud/depth.csv', depth_image)
# print('color to csv')
# ndarray_to_csv('temp_point_cloud/color.csv', color_image)

elapsed_time = time.time() - start
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
