from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
# Create your views here.

from meiduo_mall.libs.captcha.captcha import captcha

# from django.http import HttpResponse
from django import http
import logging

from meiduo_mall.libs.yuntongxun.ccp_sms import CCP

logger = logging.getLogger('django')
import random

from celery_tasks.sms.tasks import send_sms_code_func


class SMSCodeView(View):
    def get(self, request, mobile):
        '''发送短信验证码'''
        # 0.从redis中取出1的值, 查看是否存在
        # 如果1不存在, 说明60秒已过
        # 如果1存在, 说明60s以内第二次来
        redis_conn = get_redis_connection('verify_code')

        value = redis_conn.get('flag_%s' % mobile)

        if value:
            return http.JsonResponse({'code': 400,
                                      'errmsg': '请不要频繁发送短信'})

        # 1.接收参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        # 2.检验参数(整体检验 + 单个)
        # 3.整体检验
        if not all([image_code_client, uuid]):
            return http.JsonResponse({'code':400,
                                      'errmsg':'缺少必传参数'})

        # 4.单个检验, 链接redis, 创建链接对象
        # 5.利用链接对象, 获取对应的服务端的图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        # 6.判断该图形验证码是否存在
        if image_code_server is None:
            return http.JsonResponse({'code':400,
                                      'errmsg':'图形验证码过期'})

        # 5.1 删除图形验证码
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 7.对比前端和后端的图形验证码
        if image_code_client.lower() != image_code_server.decode().lower():
            return http.JsonResponse({'code': 400,
                                      'errmsg': '输入的图形验证码有误'})

        # 8.生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)

        # 创建管道:
        pl = redis_conn.pipeline()

        # 9.保存
        pl.setex('sms_%s' % mobile, 300, sms_code)

        # 制作一个定时器: 保存数据到redis: 60
        pl.setex('flag_%s' % mobile, 60, 1)

        # 执行管道:
        pl.execute()

        # 10.利用容联云, 发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # send_sms_code_func.delay(mobile, sms_code)
        logger.info('短信验证码为：%d' % sms_code)

        # 11.返回结果
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok'})


class ImageCodeView(View):

    def get(self, request, uuid):
        '''图形验证码后端接口'''
        # 1.生成图片验证码和对应的数据
        text, image = captcha.generate_captcha()

        # 2.链接redis, 获取链接对象
        redis_conn = get_redis_connection('verify_code')

        # 3.往redis中存入数据
        # redis_conn.setex('key', 'expire', 'value')
        redis_conn.setex('img_%s' % uuid, 300, text)

        # 4.返回图片
        # return HttpResponse()
        return http.HttpResponse(image, content_type='image/jpg')