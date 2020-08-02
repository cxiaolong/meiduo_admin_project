from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import ContentType
from meiduo_admin.serializers.permissions import PermissionSerializer
from meiduo_admin.serializers.permissions import ContentTypeSerializer


class PermissionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    lookup_value_regex = '\d+'

    # GET /meiduo_admin/permission/perms/ -> list
    # POST /meiduo_admin/permission/perms/ -> create
    # 思考：为什么指定权限数据的获取、修改、删除不需要实现？？？
    # GET /meiduo_admin/permission/perms/(?P<pk>\d+)/ -> retrieve
    # PUT /meiduo_admin/permission/perms/(?P<pk>\d+)/ -> update
    # DELETE /meiduo_admin/permission/perms/(?P<pk>\d+)/ -> destroy
    # GET /meiduo_admin/permission/content_types/ -> content_types

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的create
    #     return Response(serializer.data, status=201)

    # GET `/meiduo_admin/permission/content_types/`
    # @action(method=['get'], detail=False)
    def content_types(self, request):
        """
        获取权限类型数据：
        1. 获取权限类型数据
        2. 将权限类型数据序列化并返回
        """
        # 1. 获取权限类型数据
        content_types = ContentType.objects.all()

        # 2. 将权限类型数据序列化并返回
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data)





















