from goods.models import SKU
from goods.models import SKUImage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from meiduo_admin.serializers.skus import SKUImageSerializer
from meiduo_admin.serializers.skus import SKUSimpleSerializer


class SKUImageViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer


# GET /meiduo_admin/skus/simple/
class SKUSimpleView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取SKU简单数据：
        ① 查询数据库获取所有SKU的数据
        ② 将SKU数据序列化返回
        """
        # ① 查询数据库获取所有SKU的数据
        skus = SKU.objects.all()

        # ② 将SKU数据序列化返回
        serializer = SKUSimpleSerializer(skus, many=True)
        return Response(serializer.data)















