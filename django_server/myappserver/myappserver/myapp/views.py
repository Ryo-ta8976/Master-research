from myappserver.myapp.models import PointCloud
from rest_framework import viewsets
from myappserver.myapp.serializers import PointCloudSerializer


class PointCloudViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PointCloud.objects.all().order_by('id')
    serializer_class = PointCloudSerializer