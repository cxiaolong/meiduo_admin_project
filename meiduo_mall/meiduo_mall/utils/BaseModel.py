from django.db import models

class BaseModel(models.Model):
    '''模型类的基类'''

    # auto_now_add 自管理字段
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')

    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name='更新时间')

    class Meta:
        abstract = True