from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from django.db import DatabaseError


def exception_handler(exc, context):
    # 先调用DRF框架的默认异常处理函数
    response = drf_exception_handler(exc, context)

    if response is None:
        # 补充数据库的异常处理
        if isinstance(exc, DatabaseError):
            response = Response({'detail': '数据库错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
