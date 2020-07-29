from django.db import models

# Create your models here.
# 导入:
from django.db import models
from meiduo_mall.utils.BaseModel import BaseModel
from orders.models import OrderInfo


class Payment(BaseModel):
    """支付信息模型类"""

    # 交易的订单信息
    order = models.ForeignKey(OrderInfo,
                              on_delete=models.CASCADE,
                              verbose_name='订单')
    # 支付的交易号保存字段
    trade_id = models.CharField(max_length=100,
                                unique=True,
                                null=True,
                                blank=True,
                                verbose_name="支付编号")

    class Meta:
        db_table = 'tb_payment'
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name