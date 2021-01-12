import open3d as o3d
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import sys

PROCESSED_FILE_PATH = "./processed.pcd"
DISTANCE = 0.3
X_SEPARATED_NUMBER = 5
Y_SEPARATED_NUMBER = 10
SCALE = 1000
CHANGE_DEPTH_TO_MEASURED_VALUE = 39.97

# pcdファイルの読み込み
pcd = o3d.io.read_point_cloud(PROCESSED_FILE_PATH)
pcd_arr = np.asarray(pcd.points)
print(pcd)

# 各変数の初期化
all_x = []
all_y = []
grid_array = [ [[]] * Y_SEPARATED_NUMBER for i in range(X_SEPARATED_NUMBER)]
scatter_y = []
scatter_z = []
up_down = []
separated_y_arr = {}
separated_z_arr = {}

# x座標、y座標の範囲取得
for x, y, z in pcd_arr:
  all_x.append(x)
  all_y.append(y)
print("x最小値:{0} ~ x最大値:{1}".format(min(all_x), max(all_x)))
print("y最小値:{0} ~ y最大値:{1}".format(min(all_y), max(all_y)))
x_range = max(all_x) - min(all_x)
y_range = max(all_y) - min(all_y)

# grid分割
for x, y, z in pcd_arr:
  # x座標の位置決め
  for i in range(X_SEPARATED_NUMBER):
    if (x >= min(all_x) + x_range / X_SEPARATED_NUMBER * i and x <= min(all_x) + x_range / X_SEPARATED_NUMBER * (i + 1)):
      break
  # y座標の位置決め
  for j in range(Y_SEPARATED_NUMBER):
    if (y >= min(all_y) + y_range / Y_SEPARATED_NUMBER * j and y <= min(all_y) + y_range / Y_SEPARATED_NUMBER * (j + 1)):
      break
  grid_array[i][j].append([x, y, z])
print('grid分割 end')

# 統計値算出
up_down = [ [0] * Y_SEPARATED_NUMBER for i in range(X_SEPARATED_NUMBER)]
for i in range(X_SEPARATED_NUMBER):
  for j in range(Y_SEPARATED_NUMBER):
    up_down_in_grid = np.median(grid_array[i][j])
    if (up_down_in_grid > DISTANCE):
      up_down[i][j] = up_down_in_grid * SCALE / CHANGE_DEPTH_TO_MEASURED_VALUE
print('統計値算出 end')
print(up_down)

# for x, y, z in pcd_arr:
#   for i in range(SEPARATED_NUMBER):
#     if ((
#       x >= min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * i and x <= min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * (i + 1)
#       ) and (
#         abs(z) > DISTANCE
#     )):
#       if (i not in separated_y_arr):
#         separated_y_arr[i] = []
#         separated_z_arr[i] = []
#       separated_y_arr[i].append(y)
#       separated_z_arr[i].append(z)
#       break

# for i in range(SEPARATED_NUMBER):
#   print('{0} ~ {1}'.format(min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * i, min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * (i + 1)))
#   if (i in separated_z_arr):
#     print("{0}番area:起伏[{1}]\n".format(i, sum(separated_z_arr[i]) / len(separated_z_arr[i])))
#   else:
#     print('{0}番area:起伏なし\n'.format(i))


          # # 起伏の取得
          # if(abs(z) > DISTANCE):
          #     up_down.append(abs(z))
  # if len(up_down) != 0:
  #   print("{0}番area:起伏[{1}]\n".format(i, sum(up_down) / len(up_down)))
  # else:
  #   print('{0}番area:起伏なし\n'.format(i))



# for i in range(SEPARATED_NUMBER):
#   print('{0} ~ {1}'.format(min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * i, min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * (i + 1)))
#   for x, y, z in pcd_arr:
#       if (x >= min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * i and x <= min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * (i + 1)):
#           # scatter_y.append(y)
#           # scatter_z.append(z)
#           # 起伏の取得
#           if(abs(z) > DISTANCE):
#               up_down.append(abs(z))
#   if len(up_down) != 0:
#     print("{0}番area:起伏[{1}]\n".format(i, sum(up_down) / len(up_down)))
#   else:
#     print('{0}番area:起伏なし\n'.format(i))


# plt.scatter(scatter_y, scatter_z)
# plt.show()