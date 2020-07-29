# 继承自django自带的模型类
# 重写里面的authenticate函数
from django.contrib.auth.backends import ModelBackend
import re
from .models import  User







def get_user_by_account(account):
    '''判断account是用户名还是手机号, 根据获取的不同.返回user'''
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # account ===> mobile
            return User.objects.get(mobile=account)
        else:
            # acccount ===> username
            return User.objects.get(username=account)
    except Exception as e:

        return None


class UsernameMobileCountAuthencatied(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        user = get_user_by_account(username)

        if user and user.check_password(password):
            return user

