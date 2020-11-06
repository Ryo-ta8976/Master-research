from djongo import models  # djongoのモデルを利用する
import json


class PointCloud(models.Model):
    id = models.AutoField(primary_key=True)
    depth = models.CharField(max_length=200000)
    color = models.CharField(max_length=200000)
    created_at = models.DateTimeField(auto_now_add=True)

    # def set_foo(self, x):
    #     self.foo = json.dumps(x)

    # def get_foo(self):
    #     return json.loads(self.foo)
