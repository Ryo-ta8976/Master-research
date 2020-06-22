import socket
import urllib.request
import json

PORT = 5000
BUFFER_SIZE = 20000
num=0
x=""
y=""
z=""

# エンドポイント
url='http://127.0.0.1:8000/pointcloud/'
# リクエストパラメータ
params={
    'x': '[3,0,0,0,0]',
    'y': '[3,0,0,0,0]',
    'z': '[3,0,0,0,0]',
}
headers = {
    'Content-Type': 'application/json',
}
# リクエスト生成
req = urllib.request.Request(url, json.dumps(params).encode(), headers)

# with urllib.request.urlopen(req) as res:
#     body=json.load(res)

#     print(res.code)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('192.168.56.1', PORT))
    s.listen()
    while True:
        (connection, client) = s.accept()
        try:
            print('Client connected', client)
            data = connection.recv(BUFFER_SIZE)
            #print(data.decode("utf-8"))
            if(num==0):
                x+=data.decode("utf-8")
                num+=1
                print("ok")
            elif(num==1):
                y+=data.decode("utf-8")
                num+=1
            else:
                z+=data.decode("utf-8")
                num=0
            

            #connection.send(data.upper())
        finally:
            print(x)
            print(y)
            print(z)
            connection.close()