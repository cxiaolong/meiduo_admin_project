import re
from users.models import User
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


class AdminSerializer(serializers.ModelSerializer):
    """管理员用户序列化器类"""
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile',
                  'email', 'groups', 'user_permissions',
                  'password')

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                'allow_blank': True
            }
        }

    def validate_mobile(self, value):
        """手机号格式是否正确"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')

        return value


class GroupSimpleSerializer(serializers.ModelSerializer):
    """用户组简单序列化器类"""
    class Meta:
        model = Group
        fields = ('id', 'name')













