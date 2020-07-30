from users.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings


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

        attrs['user'] = user

        return attrs

    def create(self, validated_data):
        """生成jwt token """
        user = validated_data.get('user')

        # 组织payload数据的方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token数据的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 组织payload数据
        payload = jwt_payload_handler(user)
        # 生成jwt token
        token = jwt_encode_handler(payload)

        # 临时给user对象增加一个token属性
        user.token = token

        return user






















