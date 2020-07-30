from rest_framework import serializers

from users.models import User


class AdminAuthSerializer(serializers.ModelSerializer):
    """管理员登录序列化器类"""
    username = serializers.CharField(label='用户名')
    token = serializers.CharField(label='JWT token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')

        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def validate(self, attrs):
        """
        用户名和密码是否正确
        attrs: 传递给data的数据
        """
        # 获取username和password
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            # 根据username查询管理员用户
            user = User.objects.get(username=username, is_staff=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            # 校验密码是否正确
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')

        return attrs






















