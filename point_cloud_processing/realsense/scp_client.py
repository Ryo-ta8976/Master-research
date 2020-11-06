import paramiko
import scp
from datetime import datetime
import tarfile

now = datetime.now()
pcd_directory_name = now.strftime("%Y%m%d_%H%M%S")+'.tar.gz'

with tarfile.open('./store_pcd/' + pcd_directory_name, 'w:gz') as t:
    t.add('./temp_point_cloud')

print('ファイルを圧縮しました')

with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('ssh接続')
    ssh.connect(hostname='133.19.62.9',
                username='akiyama', password='InfoNetworking')

    print('SCP転送開始')
    with scp.SCPClient(ssh.get_transport(), socket_timeout=10) as scp:
        scp.put("./store_pcd/" + pcd_directory_name, "store_pcd/" + now.strftime("%Y%m") + "/" + pcd_directory_name)

    ssh.close()

print("アップロードしました")
