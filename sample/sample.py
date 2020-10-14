import requests

# Djangoサーバエンドポイント
url = 'http://127.0.0.1:8000/pointcloud/1'

with requests.get(url) as res:
    print(res.content[:500])
