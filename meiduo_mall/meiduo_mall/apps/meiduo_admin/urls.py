from django.urls import path
from meiduo_admin.views import users
from meiduo_admin.views import statistical

urlpatterns = [
    # 进行url配置
    path('authorizations/', users.AdminAuthView.as_view()),
    path('statistical/day_active/', statistical.UserDayActiveView.as_view()),
    path('statistical/day_orders/', statistical.UserDayOrdersView.as_view()),
    path('statistical/month_increment/', statistical.UserMonthCountView.as_view()),
    path('users/', users.UserInfoView.as_view()),
]































