import open3d as o3d

PROCESSED_FILE_PATH = "./reduced_pc_1203_2.pcd"

# 点群のビジュアライズ
print("Load a ply point cloud, print it, and render it")
pcd = o3d.io.read_point_cloud(PROCESSED_FILE_PATH)
print(pcd)
# 軸オブジェクトの生成
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=1, origin=[0, 0, 0])
o3d.visualization.draw_geometries([pcd, mesh_frame])