from users.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


# GET /meiduo_admin/statistical/day_active/
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




























