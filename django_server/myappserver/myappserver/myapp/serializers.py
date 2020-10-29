from myappserver.myapp.models import PointCloud
from rest_framework import serializers


class PointCloudSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PointCloud
        fields = ['id', 'x', 'y', 'z', 'created_at']
