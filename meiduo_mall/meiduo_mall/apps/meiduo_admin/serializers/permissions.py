from rest_framework import serializers
from django.contrib.auth.models import Group
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


class GroupSerializer(serializers.ModelSerializer):
    """用户组序列化器类"""
    class Meta:
        model = Group
        fields = '__all__'


class PermSimpleSerializer(serializers.ModelSerializer):
    """权限简单序列化器类"""
    class Meta:
        model = Permission
        fields = ('id', 'name')
















