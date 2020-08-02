from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器类"""
    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    """权限类型序列化器类"""
    class Meta:
        model = ContentType
        fields = ('id', 'name')



















