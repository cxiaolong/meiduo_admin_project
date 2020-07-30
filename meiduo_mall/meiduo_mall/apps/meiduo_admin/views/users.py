from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from meiduo_admin.serializers.users import AdminAuthSerializer


# POST /meiduo_admin/authorizations/
class AdminAuthView(APIView):
    def post(self, request):
        """
        管理员登录:
        1. 获取参数并进行校验(参数完整性、用户名和密码是否正确)
        2. 服务器需要生成jwt token
        3. 返回响应数据,登录成功
        """
        serializer = AdminAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data.get('username')
        user = User.objects.get(username=username)

        # 组织payload数据的方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token数据的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 组织payload数据
        payload = jwt_payload_handler(user)
        # 生成jwt token
        token = jwt_encode_handler(payload)

        response_data = {
            'id': user.id,
            'username': user.username,
            'token': token
        }

        return Response(response_data)































