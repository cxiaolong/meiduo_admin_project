from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer, BadData
from django.conf import settings

# Create your models here.
from meiduo_mall.utils.BaseModel import BaseModel


class User(AbstractUser):
    """用户模型类"""
    # 添加手机字段:
    mobile = models.CharField(max_length=11,
                              unique=True,
                              verbose_name='手机号')

    # 再新增一个记录邮箱是否激活的字段
    email_active = models.BooleanField(default=False,
                                       verbose_name='邮箱激活')

    # 新增
    default_address = models.ForeignKey('Address',
                                        related_name='users',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL,
                                        verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # 生成验证链接的函数:
    def generate_verify_url(self):
        """返回验证链接verify_url"""
        obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=3600)
        dict = {
            'user_id': self.id,
            'email': self.email
        }

        token = obj.dumps(dict).decode()

        verify_url = settings.EMAIL_VERIFY_URL + token

        return verify_url

    @staticmethod
    def check_verify_url_token(token):
        """把token解密, 返回user"""
        obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=3600)

        try:
            dict = obj.loads(token)
        except BadData:
            return None

        user_id = dict.get('user_id')
        email = dict.get('email')

        try:
            user = User.objects.get(id=user_id,
                                    email=email)
        except Exception as e:
            return None
        else:
            return user


# 增加地址的模型类, 放到User模型类的下方:
class Address(BaseModel):
    """用户地址模型类"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='addresses',
                             verbose_name='用户')

    province = models.ForeignKey('areas.Area',
                                 on_delete=models.PROTECT,
                                 related_name='province_addresses',
                                 verbose_name='省')

    city = models.ForeignKey('areas.Area',
                             on_delete=models.PROTECT,
                             related_name='city_addresses',
                             verbose_name='市')

    district = models.ForeignKey('areas.Area',
                                 on_delete=models.PROTECT,
                                 related_name='district_addresses',
                                 verbose_name='区')

    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    phone = models.CharField(max_length=20,
                             null=True,
                             blank=True,
                             default='',
                             verbose_name='固定电话')

    email = models.CharField(max_length=30,
                             null=True,
                             blank=True,
                             default='',
                             verbose_name='电子邮箱')

    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_addresses'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']








