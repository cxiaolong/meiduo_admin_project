from users.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


# GET /meiduo_admin/statistical/day_active/
# 通过请求头传递jwt token, 给jwt扩展包使用
# 格式: Authorization: jwt <jwt token>
class UserDayActiveView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        统计网站日活跃用户的数量:
        1. 查询User表当日活跃用户数量
        2. 返回统计之后的结果
        """
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()

        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/day_orders/
class UserDayOrdersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取日下单用户数量：
        1. 获取日下单用户数量
        2. 返回应答
        """
        # 1. 获取日下单用户数量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(orders__create_time__gte=now_date).distinct().count()

        # 2. 返回应答
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/month_increment/
class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取近30天网站每日新增用户数据:
        1. 查询数据库统计网站近30天每日新增用户数量
        2. 返回响应数据
        """
        # 1. 查询数据库统计网站近30天每日新增用户数量
        # 结束时间
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 起始时间: now_date - 29天
        begin_date = now_date - timezone.timedelta(days=29)

        # 当天日期
        current_date = begin_date

        # 新增用户的数量
        month_li = []

        while current_date <= now_date:
            # 次日时间
            next_date = current_date + timezone.timedelta(days=1)
            # 统计当天的新增用户数量
            count = User.objects.filter(date_joined__gte=current_date,
                                        date_joined__lt=next_date).count()

            month_li.append({
                'count': count,
                'date': current_date.date()
            })

            current_date = next_date

        # 2. 返回应答
        return Response(month_li)
























