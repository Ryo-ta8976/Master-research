import socket
import urllib.request
import json
import requests

PORT = 5555
BUFFER_SIZE = 1024
num = 0
x = ""
y = ""
z = ""

# Djangoサーバエンドポイント
url = 'http://127.0.0.1:8000/pointcloud/'
headers = {
    'Content-Type': 'application/json',
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('192.168.56.1', PORT))
    s.listen()
    while True:
        print("waiting...")
        (connection, client) = s.accept()
        try:
            print('Client connected', client)
            data_sum = ''
            count = 0
            while True:
                data = connection.recv(BUFFER_SIZE)  # 1024バイトづつ分割して受信する
                data_sum = data_sum + data.decode("utf-8")  # 受信した分だけ足していく
                count += 1
                if not data:
                    print("データ量:"+str((1024*count)/1000)+"kbyte")
                    count = 0
                    break
            # print(data_sum) #受信したデータを表示

            # print(data.decode("utf-8"))
            if(num == 0):
                # x+=data_sum.decode("utf-8")
                x = data_sum
                num += 1
                print("x")
                print(len(x))
                # print(x)
            elif(num == 1):
                y = data_sum
                num += 1
                print("y")
                print(len(y))
            else:
                z = data_sum

                print("z")
                print(len(z))

                # リクエストパラメータ
                data = {
                    'x': x,
                    'y': y,
                    'z': z,
                }

                # params={
                #     'x': "4,0,0,0,0",
                #     'y': "4,0,0,0,0",
                #     'z': "4,0,0,0,0",
                # }

                # リクエスト生成
                # req = urllib.request.Request(url, json.dumps(params).encode(), headers)

                # with urllib.request.urlopen(req) as res:
                #     body=json.load(res)

                #     print(res.code)

                with requests.post(url, headers=headers, json=data) as res:
                    print(res.status_code)
                    # print(res.content)

                # データの初期化
                x = ""
                y = ""
                z = ""
                num = 0

            # connection.send(data.upper())
        finally:
            connection.close()
