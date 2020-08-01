from goods.models import SKUImage
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.skus import SKUImageSerializer


class SKUImageViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer

















