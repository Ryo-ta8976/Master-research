import requests
import json
import numpy as np
import open3d as o3d

# Djangoサーバエンドポイント
url = 'http://127.0.0.1:8000/pointcloud/7'
headers = {
    'Content-Type': 'application/json',
}

with requests.get(url, headers=headers) as res:
    data = res.json()
    x = data["x"].split((','))
    y = data["y"].split((','))
    z = data["z"].split((','))

    temp_x_y_z = []
    for i in range(len(x)):
        temp_x_y_z.append([x[i], y[i], z[i]])
    np_x_y_z = np.array(temp_x_y_z)

    # 点群のpoint cloud オブジェクト化
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np_x_y_z)
    o3d.io.write_point_cloud("./mongodb.pcd", pcd)

    pcd = o3d.io.read_point_cloud("./mongodb.pcd")
    # 軸オブジェクトの生成
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=1000, origin=[0, 0, 0])
    # 点群の可視化
    o3d.visualization.draw_geometries([pcd, mesh_frame])
