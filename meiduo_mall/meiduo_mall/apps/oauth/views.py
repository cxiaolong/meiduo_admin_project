from QQLoginTool.QQtool import OAuthQQ
from django.contrib.auth import login
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import JsonResponse
import json, re

from carts.utils import merge_cart_cookie_to_redis
from oauth.models import OAuthQQUser
from oauth.utils import generate_access_token, check_access_token
from django_redis import get_redis_connection

from users.models import User


class OAuthUserView(View):

    def get(self, request):
        '''oauth2.0认证'''
        # 1.接收code参数(查询字符串)
        code = request.GET.get('code')

        # 2.判断该参数是否存在
        if not code:
            return JsonResponse({'code':400,
                                 'errmsg':"缺少code参数"})

        # 3.生成QQLoginTool工具类对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,)


        try:
            # 4.调用对象的方法, 发送请求, 获取access_token
            access_token = oauth.get_access_token(code)

            # 5.把token作为参数,再次发送请求, 获取openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':"给qq发送请求失败"})


        # 6.把openid作为条件在OAuthQQUser中检索. 获取对象
        try:
            oauth_qq = OAuthQQUser.objects.get(openid=openid)
        except Exception as e:
            # 11.把openid加密为access_token
            access_token = generate_access_token(openid)

            # 12.把access_token返回
            return JsonResponse({'code':300,
                                 'errmsg':"ok",
                                 'access_token':access_token})

        else:
            # 7.如果能拿到OAuthQQUser的对象(说明对象存在)
            user = oauth_qq.user

            # 8.状态保持
            login(request, user)

            response = JsonResponse({'code':0,
                                     'errmsg':'ok'})

            # 9.设置cookie中的username
            response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

            # 补充内容:购物车的合并
            response = merge_cart_cookie_to_redis(request, response)


            # 10.返回响应
            return response


    def post(self, request):
        '''保存表单时数据'''
        # 1.接收参数
        dict = json.loads(request.body.decode())
        mobile = dict.get('mobile')
        password = dict.get('password')
        sms_code_client = dict.get('sms_code')
        access_token = dict.get('access_token')

        # 2.检验参数(整体 + 单个)
        # 3.整体
        if not all([mobile, password, sms_code_client, access_token]):
            return JsonResponse({'code':400,
                                 'errmsg':"缺少必传参数"})

        # 4.mobile单个检验
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': "mobile格式不正确"})

        # 5.password单个检验
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({'code': 400,
                                 'errmsg': "password格式不正确"})

        # 6.链接redis, 获取链接对象
        redis_conn = get_redis_connection('verify_code')

        # 7.从redis中获取短信验证码
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        # 8.判断该短信验证码是否存在
        if not sms_code_server:
            return JsonResponse({'code': 400,
                                 'errmsg': "短信验证码过期"})

        # 9.对比前后端的短信验证码
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400,
                                 'errmsg': "输入的短信验证吗有误"})

        # 10.把access_token解密为openid
        openid = check_access_token(access_token)

        # 11.根据mobile,去User表中查询是否存在用户
        try:
            user = User.objects.get(mobile=mobile)
        except Exception as e:
            # 13.如果不存在, 往User表中增加一个新用户
            user = User.objects.create_user(username=mobile,
                                            password=password,
                                            mobile=mobile)
        else:
            # 12.如果存在, 检查密码
            if not user.check_password(password):
                return JsonResponse({'code': 400,
                                     'errmsg': "输入的密码不正确"})

        # 14.往QQ表中存储数据(user , openid)
        try:
            OAuthQQUser.objects.create(user=user,
                                       openid=openid)
        except Exception as  e:
            return JsonResponse({'code': 400,
                                 'errmsg': "往数据库写入数据失败"})

        # 15.状态保持
        login(request, user)

        response = JsonResponse({'code':0,
                                 'errmsg':'ok'})

        # 16.往cookie中写入用户名(username)
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        # 补充内容:购物车的合并
        response = merge_cart_cookie_to_redis(request, response)

        # 17.返回json
        return response




# Create your views here.
class OAuthURLView(View):

    def get(self, request):
        '''qq登录的第一个接口'''
        # 1.获取next参数
        next = request.GET.get('next')

        # 2.获取QQLoginTool的对象
        # 创建对象
        # 创建对象的时候, 需要传递四个参数:
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)

        # 3.通过获取的对象, 获得qq服务器的地址
        login_url = oauth.get_qq_url()

        # 4.拼接json参数, 返回
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'login_url':login_url})
