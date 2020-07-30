from django.urls import path
from meiduo_admin.views import users

urlpatterns = [
    # 进行url配置
    path(r'authorizations/', users.AdminAuthView.as_view()),
]