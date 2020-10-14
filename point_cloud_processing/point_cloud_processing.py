import open3d as o3d
import numpy as np
import math
import time
import matplotlib.pyplot as plt

# 平面と点の距離閾値
DISTANCE = 0.01

# 点群のビジュアライズ
print("Load a ply point cloud, print it, and render it")
pcd = o3d.io.read_point_cloud("./mongodb.pcd")
print(pcd)
print(np.asarray(pcd.points))
# 軸オブジェクトの生成
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=1000, origin=[0, 0, 0])
o3d.visualization.draw_geometries([pcd, mesh_frame])


# 点群の平面抽出
t1 = time.time()
before_pcd = o3d.io.read_point_cloud("./mongodb.pcd")
plane_model, inliers = before_pcd.segment_plane(distance_threshold=DISTANCE,
                                                ransac_n=3,
                                                num_iterations=1000)
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
t2 = time.time()

# inlier_cloud = before_pcd.select_by_index(inliers)
# inlier_cloud.paint_uniform_color([1.0, 0, 0])
# outlier_cloud = before_pcd.select_by_index(inliers, invert=True)
# o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])


# 平面上の点Pの選択
t3 = time.time()
out_arr = np.asarray(before_pcd.points)
for x, y, z in out_arr:
    if(abs(a*x+b*y+c*z+d)/math.sqrt(a*a+b*b+c*c) < DISTANCE):
        Py = y
        Pz = z
        break

Px = (-b*Py-c*Pz-d)/a

# 法線ベクトルの取得
nx = a
ny = b
nz = c


# なす角の計算
theta = math.acos(nz/math.sqrt(nx*nx+ny*ny+nz*nz))
if(ny >= 0):
    phi = math.acos(nx/math.sqrt(nx*nx+ny*ny))
else:
    phi = math.acos(nx/math.sqrt(nx*nx+ny*ny))+math.pi

print(theta)
print(phi)


# 回転行列の生成
y_arr = np.matrix([[math.cos(-theta), 0, math.sin(-theta)],
                   [0, 1, 0], [-1*math.sin(-theta), 0, math.cos(-theta)]])
print(y_arr)
z_arr = np.matrix([[math.cos(-phi), -1*math.sin(-phi), 0],
                   [math.sin(-phi), math.cos(-phi), 0], [0, 0, 1]])
print(z_arr)


# 点群のアフィン変換
processed_arr = np.array([[0, 0, 0]])
for x, y, z in out_arr:
    # 平行移動
    arr = np.array([[x-Px, y-Py, z-Pz]])
    # 回転移動
    arr = np.dot(arr, z_arr)
    arr = np.dot(arr, y_arr)
    # 回転後の点群配列の生成
    processed_arr = np.append(processed_arr, arr, axis=0)

processed_arr = np.delete(processed_arr, 0, 0)
print(processed_arr.shape)
t4 = time.time()


# 点群のpoint cloud オブジェクト化
after_pcd = o3d.geometry.PointCloud()
after_pcd.points = o3d.utility.Vector3dVector(processed_arr)
o3d.io.write_point_cloud("./processed.pcd", after_pcd)


result_pcd = o3d.io.read_point_cloud("./processed.pcd")
# mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
#         size=1000, origin=[0, 0, 0])
o3d.visualization.draw_geometries([result_pcd, mesh_frame])
print("平面抽出：{0}".format(t2-t1))
print("アフィン変換：{0}".format(t4-t3))


# グラフ表示
yy = []
zz = []
xx = []
up_down = []
processed_arr = np.array(processed_arr)
for x, y, z in processed_arr:
    xx.append(x)
    if(x > 100 and x < 300):
        print(y)
        print(z)
        yy.append(y)
        zz.append(z)
        # 起伏の計算
        if(abs(z) > 100):
            print("up down")
            up_down.append(abs(z))
print("最小値:{0}".format(min(xx)))
print("最大値:{0}".format(max(xx)))
if len(up_down) != 0:
    print("起伏:{0}".format(sum(up_down)/len(up_down)))

plt.scatter(yy, zz)
plt.show()
