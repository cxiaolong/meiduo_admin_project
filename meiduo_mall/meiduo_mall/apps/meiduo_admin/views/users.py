from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from meiduo_admin.serializers.users import AdminAuthSerializer


# POST /meiduo_admin/authorizations/
class AdminAuthView(APIView):
    def post(self, request):
        """
        管理员登录:
        1. 获取参数并进行校验(参数完整性、用户名和密码是否正确)
        2. 服务器需要生成jwt token
        3. 返回响应数据,登录成功
        直接继承CreateAPIView
        from rest_framework.generics import CreateAPIView
        class AdminAuthView(CreateAPIView):
            serializer_class = AdminAuthSerializer
        """
        serializer = AdminAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)































