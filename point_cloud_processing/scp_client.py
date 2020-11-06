import paramiko
import scp
from datetime import datetime

now = datetime.now()

with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='133.19.62.9',
                username='akiyama', password='InfoNetworking')

    # scp clientオブジェクト生成
    with scp.SCPClient(ssh.get_transport()) as scp:
        scp.get("store_pcd/202011/20201106_152639.tar.gz", "pcd/20201106_152639.tar.gz")
