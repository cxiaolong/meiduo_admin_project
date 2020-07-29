from django.db import models

# Create your models here.
from meiduo_mall.utils.BaseModel import BaseModel


class ContentCategory(BaseModel):
    """广告类别表"""
    # 广告类别名称
    name = models.CharField(max_length=50,
                            verbose_name='名称')
    # 广告的类别键名:
    key = models.CharField(max_length=50,
                           verbose_name='类别键名')

    class Meta:
        db_table = 'tb_content_category'
        verbose_name = '广告内容类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Content(BaseModel):
    """广告内容表"""

    # 外键, 关联广告类别
    category = models.ForeignKey(ContentCategory,
                                 on_delete=models.PROTECT,
                                 verbose_name='类别')
    # 广告标题
    title = models.CharField(max_length=100,
                             verbose_name='标题')
    # 广告被点击后跳转的 url
    url = models.CharField(max_length=300,
                           verbose_name='内容链接')
    # 广告图片地址保存字段:
    image = models.ImageField(null=True,
                              blank=True,
                              verbose_name='图片')
    # 文字性广告保存在该字段:
    text = models.TextField(null=True,
                            blank=True,
                            verbose_name='内容')
    # 广告内容排序:
    sequence = models.IntegerField(verbose_name='排序')
    # 广告是否展示的状态:
    status = models.BooleanField(default=True,
                                 verbose_name='是否展示')

    class Meta:
        db_table = 'tb_content'
        verbose_name = '广告内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name + ': ' + self.title