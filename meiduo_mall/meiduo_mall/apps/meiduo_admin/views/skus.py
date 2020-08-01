from goods.models import SKU
from goods.models import SKUImage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from meiduo_admin.serializers.skus import SKUImageSerializer
from meiduo_admin.serializers.skus import SKUSimpleSerializer


class SKUImageViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer


# GET /meiduo_admin/skus/simple/
class SKUSimpleView(ListAPIView):
    queryset = SKU.objects.all()
    permission_classes = [IsAdminUser]
    # 关闭分页
    pagination_class = None















