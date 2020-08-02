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

    def create(self, validated_data):
        """保存新增管理员用户的数据"""
        # 添加管理员标记
        validated_data['is_staff'] = True
        # 1. 保存新增管理员的其他数据(除了password)
        user = super().create(validated_data)

        # 2. 判断是否需要设置默认密码,以及密码加密保存
        password = validated_data.get('password')
        # 当password为None或者为''空字符串时
        if not password:
            # 设置默认密码
            password = '123456abc'
        user.set_password(password)
        user.save()

        return user

    # 密码修改,需要重写
    def update(self, instance, validated_data):
        # 修改管理员用户的其他数据(除: password)
        password = validated_data.pop('password', None)
        super().update(instance, validated_data)

        # 判断密码是否需要进行修改,修改密码
        if password:
            instance.set_password(password)
            instance.save()

        return instance


class GroupSimpleSerializer(serializers.ModelSerializer):
    """用户组简单序列化器类"""
    class Meta:
        model = Group
        fields = ('id', 'name')













