from django.urls import path
from meiduo_admin.views import skus
from meiduo_admin.views import users
from meiduo_admin.views import statistical

urlpatterns = [
    # 进行url配置
    path('authorizations/', users.AdminAuthView.as_view()),
    path('statistical/day_active/', statistical.UserDayActiveView.as_view()),
    path('statistical/day_orders/', statistical.UserDayOrdersView.as_view()),
    path('statistical/month_increment/', statistical.UserMonthCountView.as_view()),
    path('users/', users.UserInfoView.as_view()),
    # SKU图片管理
    path('skus/images/', skus.SKUImageViewSet.as_view({
        'get': 'list'
    })),
    path('skus/simple/', skus.SKUSimpleView.as_view()),
]































