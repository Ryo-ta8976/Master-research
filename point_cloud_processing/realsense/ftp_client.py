from datetime import datetime
import tarfile
import paramiko

now = datetime.now()
pcd_directory_name = now.strftime("%Y%m%d_%H%M%S") + '.tar.gz'

with tarfile.open('./store_pcd/' + pcd_directory_name, 'w:gz') as t:
    t.add('./temp_point_cloud')

print('ファイルを圧縮しました')

# SFTP接続先の設定
HOST = "133.19.62.9"
PORT = 22
SFTP_USER = "akiyama"
SFTP_PASSWORD = 'InfoNetworking'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(HOST, port=PORT, username=SFTP_USER, password=SFTP_PASSWORD)
try:
    # SFTPセッション開始
    sftp_connection = client.open_sftp()

    # ファイルの転送
    sftp_connection.put("./store_pcd/" + pcd_directory_name, "store_pcd/" + now.strftime("%Y%m") + "/" + pcd_directory_name)
    print('ファイルを転送しました')
finally:
    client.close()