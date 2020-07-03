import open3d as o3d
import numpy as np

# 点群のビジュアライズ
# print("Load a ply point cloud, print it, and render it")
# pcd = o3d.io.read_point_cloud("./test_pcd.pcd")
# print(pcd)
# print(np.asarray(pcd.points))
# o3d.visualization.draw_geometries([pcd])


# 点群の平面抽出
pcd = o3d.io.read_point_cloud("./test_pcd.pcd")
plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,
                                         ransac_n=3,
                                         num_iterations=1000)
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

inlier_cloud = pcd.select_by_index(inliers)
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud = pcd.select_by_index(inliers, invert=True)
o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])