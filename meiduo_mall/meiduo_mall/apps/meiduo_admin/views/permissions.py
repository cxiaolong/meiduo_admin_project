from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAdminUser
from meiduo_admin.serializers.permissions import PermissionSerializer


class PermissionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer





















