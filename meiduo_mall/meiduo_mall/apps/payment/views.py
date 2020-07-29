from alipay import AliPay
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
# Create your views here.
from orders.models import OrderInfo
import os

from payment.models import Payment


class PaymentStatusView(View):
    
    def put(self, request):
        '''接收请求,进行校验, 保存结果'''
        # 1.接收参数(查询字符串参数)
        query_dict = request.GET
        dict = query_dict.dict()

        # 2.从查询字符串参数剔除sign字段, 获取sign对应的value部分
        signature = dict.pop('sign')

        # 3.获取python-alipay-sdk框架的对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "keys/alipay_public_key.pem"),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )
        # 4.调用对象的验证函数verify()
        success = alipay.verify(dict, signature)

        # 5.判断结果,
        if success:
            order_id = dict.get('out_trade_no')
            trade_id = dict.get('trade_no')
            # 如果为true. 保存订单号和流水号到数据库中
            Payment.objects.create(
                order_id=order_id,
                trade_id=trade_id
            )
            # 6.更改订单的状态 (未支付 ===> 待评价)
            OrderInfo.objects.filter(order_id=order_id,
                                     status=1).update(status=4)

            return JsonResponse({'code':0,
                                 'errmsg':'ok',
                                 'trade_id':trade_id})
        else:
            # 7.如果为false ====> 非法请求, 报错
            return JsonResponse({'code':400,
                                 'errmsg':"非法请求"})


class PaymentView(View):
    def get(self, request, order_id):
        '''接收order_id,返回支付宝的登录链接'''
        # 1.检验参数, 把order_id转为order
        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                  user=request.user,
                                  status=1)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'order_id有误'})

        # 2.调用python-alipay-sdk框架的类,生成对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "keys/alipay_public_key.pem"),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )
        # 3.调用对象的函数, 拼接查询字符串参数
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject="美多商城%s" % order_id,
            return_url=settings.ALIPAY_RETURN_URL,
        )
        # 4.url的前部分 + ? + 查询字符串参数 共同组成完整的url
        url = settings.ALIPAY_URL + '?' + order_string

        # 5.把url拼接, 形成json, 返回
        return JsonResponse({'code':0,
                             'errmsg':"ok",
                             'alipay_url':url})
