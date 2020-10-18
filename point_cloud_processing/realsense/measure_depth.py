import pyrealsense2 as rs
import numpy as np
import cv2
import datetime
import os

# ストリーム(Color/Depth)の設定
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

# 距離の計算 距離[m] = depth * depth_scale
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# レーザー出力の設定(0~100)
set_laser = 100
depth_sensor.set_option(rs.option.laser_power, set_laser)
# レーザー出力の確認
laser_pwr = depth_sensor.get_option(rs.option.laser_power)
print("laser power = ", laser_pwr)

# 抽出範囲（meter）
clipping_distance_in_meters_min = 0.11  # meter
clipping_distance_in_meters_max = 0.65  # meter

clipping_distance_min = clipping_distance_in_meters_min / depth_scale
clipping_distance_max = clipping_distance_in_meters_max / depth_scale

image_num = 0
today = datetime.date.today()
today_str = str(today)
store_path = "./images/" + today_str

try:
    while True:
        # フレーム待ち(Depth)
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # Depth画像
        depth_color_frame = rs.colorizer().colorize(depth_frame)
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_image_3d = np.dstack((depth_image, depth_image, depth_image))
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        bg_removed = np.where((depth_image_3d > clipping_distance_min) & (
            depth_image_3d < clipping_distance_max), depth_color_image, 0)
        bg_removed_uint8 = np.asanyarray(bg_removed, dtype=np.uint8)

        # 表示
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', bg_removed_uint8)

        key = cv2.waitKey(1) & 0xff
        # sキーでキャプチャ
        if key == ord('s'):
            os.makedirs(store_path, exist_ok=True)  # 今日の日付でフォルダを生成
            filename = store_path + '/' + str(image_num) + '.png'
            cv2.imwrite(filename, bg_removed_uint8)
            print(filename + 'を保存しました')
            image_num += 1
        # escキーで終了
        elif key == 27:
            break

finally:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()
