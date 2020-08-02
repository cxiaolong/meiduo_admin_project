from users.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import ContentType
from meiduo_admin.serializers.permissions import AdminSerializer
from meiduo_admin.serializers.permissions import GroupSerializer
from meiduo_admin.serializers.permissions import PermissionSerializer
from meiduo_admin.serializers.permissions import PermSimpleSerializer
from meiduo_admin.serializers.permissions import ContentTypeSerializer
from meiduo_admin.serializers.permissions import GroupSimpleSerializer


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


class GroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # GET /meiduo_admin/permission/groups/ -> list
    # POST /meiduo_admin/permission/groups/ -> create
    # GET /meiduo_admin/permission/groups/(?P<pk>\d+)/ -> retrieve
    # PUT /meiduo_admin/permission/groups/(?P<pk>\d+)/ -> update
    # DELETE /meiduo_admin/permission/groups/(?P<pk>\d+)/ -> destroy
    # GET /meiduo_admin/permission/simple/ -> simple

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的create
    #     return Response(serializer.data, status=201)

    def simple(self, request):
        """
        获取权限的简单数据
        """
        perms = Permission.objects.all()
        serializer = PermSimpleSerializer(perms, many=True)
        return Response(serializer.data)


class AdminViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminSerializer
    # GET /meiduo_admin/permission/admins/ -> list

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的create
    #     return Response(serializer.data, status=201)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的update
    #     return Response(serializer.data)

    def simple(self, request):
        """
        获取用户组的简单数据：
        ① 查询数据库获取所有用户组数据
        ② 将用户组数据序列化并返回
        """
        # ① 查询数据库获取所有用户组数据
        groups = Group.objects.all()

        # ② 将用户组数据序列化并返回
        serializer = GroupSimpleSerializer(groups, many=True)
        return Response(serializer.data)




































