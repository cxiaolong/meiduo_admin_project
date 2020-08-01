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

    # GET /meiduo_admin/skus/images/ -> list
    # POST /meiduo_admin/skus/images/ -> create

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的create
    #     return Response(serializer.data, status=201)


# GET /meiduo_admin/skus/simple/
class SKUSimpleView(ListAPIView):
    queryset = SKU.objects.all()
    permission_classes = [IsAdminUser]
    # 关闭分页
    pagination_class = None















