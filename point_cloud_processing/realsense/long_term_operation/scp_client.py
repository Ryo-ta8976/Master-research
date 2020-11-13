import paramiko
import scp
from datetime import datetime
import tarfile
import log
import os
import subprocess


now = datetime.now()
pcd_directory_name = now.strftime("%Y%m%d_%H%M%S") + '.tar.gz'


def compress_file():
    with tarfile.open('../store_pcd/' + pcd_directory_name, 'w:gz') as t:
        t.add('../temp_point_cloud')

    print('ファイルを圧縮しました')
    log.log('ファイルを圧縮しました')


def check_directory_exist():
    if not (os.path.exists('../../../ssd/akiyama/{}'.format(now.strftime("%Y%m")))):
        cmd = 'mkdir ../../../ssd/akiyama/{}'.format(now.strftime("%Y%m"))
        subprocess.call(cmd, shell=True)
    if not (os.path.exists('../../../ssd/akiyama/{}/{}'.format(now.strftime("%Y%m"), now.strftime("%m%d")))):
        cmd = 'mkdir ../../../ssd/akiyama/{}/{}'.format(now.strftime("%Y%m"), now.strftime("%m%d"))
        subprocess.call(cmd, shell=True)
    if not (os.path.exists('../../../ssd/akiyama/{}/{}/{}'.format(now.strftime("%Y%m"), now.strftime("%m%d"), now.strftime("%d%H")))):
        cmd = 'mkdir ../../../ssd/akiyama/{}/{}/{}'.format(now.strftime("%Y%m"), now.strftime("%m%d"), now.strftime("%d%H"))
        subprocess.call(cmd, shell=True)


def copy_compressed_file_to_ssd():
    # path = os.path.dirname(os.path.abspath(__file__))
    cmd = 'sudo cp ../store_pcd/{} ../../../ssd/akiyama/{}/{}/{}/{}'.format(pcd_directory_name, now.strftime("%Y%m"), now.strftime("%m%d"), now.strftime("%d%H"), pcd_directory_name)
    subprocess.call(cmd, shell=True)
    print('ファイルをコピーしました')
    log.log('ファイルをコピーしました')


def delete_comporessed_file():
    cmd = 'rm -r ../store_pcd/{}'.format(pcd_directory_name)
    subprocess.call(cmd, shell=True)
    print('元のファイルを削除しました')
    log.log('元のファイルを削除しました')


def send_file_to_server():
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('ssh接続')
        ssh.connect(hostname='133.19.62.9',
                    username='akiyama', password='InfoNetworking')

        print('SCP転送開始')
        with scp.SCPClient(ssh.get_transport(), socket_timeout=10) as scp_client:
            scp_client.put("../../../ssd/akiyama/{}/{}/{}/{}".format(now.strftime("%Y%m"), now.strftime("%m%d"), now.strftime("%d%H"), pcd_directory_name), "store_pcd/" + now.strftime("%Y%m") + "/" + pcd_directory_name)

        ssh.close()

    print("アップロードしました")
    log.log('アップロードしました')


def main():
  compress_file()
  check_directory_exist()
  copy_compressed_file_to_ssd()
  delete_comporessed_file()
  send_file_to_server()


if __name__ == '__main__':
    main()