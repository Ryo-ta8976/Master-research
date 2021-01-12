import open3d as o3d
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import sys

PROCESSED_FILE_PATH = "./processed.pcd"
DISTANCE = 0.3
SEPARATED_NUMBER = 10

pcd = o3d.io.read_point_cloud(PROCESSED_FILE_PATH)
pcd_arr = np.asarray(pcd.points)
print(pcd)

all_x = []
scatter_y = []
scatter_z = []
up_down = []
separated_y_arr = {}
separated_z_arr = {}

# x座標の範囲取得
for x, y, z in pcd_arr:
  all_x.append(x)
print("最小値:{0}".format(min(all_x)))
print("最大値:{0}".format(max(all_x)))

for x, y, z in pcd_arr:
  for i in range(SEPARATED_NUMBER):
    if ((
      x >= min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * i and x <= min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * (i + 1)
      ) and (
        abs(z) > DISTANCE
    )):
      if (i not in separated_y_arr):
        separated_y_arr[i] = []
        separated_z_arr[i] = []
      separated_y_arr[i].append(y)
      separated_z_arr[i].append(z)
      break

for i in range(SEPARATED_NUMBER):
  print('{0} ~ {1}'.format(min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * i, min(all_x) + (max(all_x) - min(all_x)) / SEPARATED_NUMBER * (i + 1)))
  if (i in separated_z_arr):
    print("{0}番area:起伏[{1}]\n".format(i, sum(separated_z_arr[i]) / len(separated_z_arr[i])))
  else:
    print('{0}番area:起伏なし\n'.format(i))


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