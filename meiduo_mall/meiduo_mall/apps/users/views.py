from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from django.views import View

from carts.utils import merge_cart_cookie_to_redis
from goods.models import SKU
from meiduo_mall.utils.views import LoginRequiredMixin
from .models import User, Address
from django.http import JsonResponse
import json, re
from django_redis import get_redis_connection
from celery_tasks.email.tasks import send_verify_email


class SaveHistoryView(View):
    def post(self, request):
        '''保存用户浏览记录'''
        # 1.接收json参数
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')

        # 2.检验sku_id是否正确
        try:
            SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'sku_id验证失败'})

        # 3.链接redis, 获取链接对象
        redis_conn = get_redis_connection('history')
        pl = redis_conn.pipeline()
        user_id = request.user.id

        # 4.删除redis中的sku_id数据
        pl.lrem('history_%s' % user_id, 0, sku_id)

        # 5.增加sku_id数据
        pl.lpush('history_%s' % user_id, sku_id)

        # 6.保留5个商品数据
        pl.ltrim('history_%s' % user_id, 0, 4)

        pl.execute()

        # 7.返回结果
        return JsonResponse({'code': 0,
                             'errmsg': 'ok'})


class ChangePasswordView(View):
    def put(self, request):
        '''修改密码'''
        # 1.接收json的参数
        dict = json.loads(request.body.decode())
        old_password = dict.get('old_password')
        new_password = dict.get('new_password')
        new_password2 = dict.get('new_password2')

        # 2.整体检验, 查看三个参数是否齐全
        if not all([old_password, new_password, new_password2]):
            return JsonResponse({'code':400,
                                 'errmsg':'缺少必传参数'})

        # 3.验证老密码是否正确, 获取结果
        result = request.user.check_password(old_password)

        # 4.判断结果是否存在, 如果不存在, 返回
        if not result:
            return JsonResponse({'code': 400,
                                 'errmsg': '老密码错误'})

        # 5.检验新密码是否满足格式要求
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({'code': 400,
                                 'errmsg': '新密码不满足格式要求'})

        # 6.检验两个新密码是否一致
        if new_password != new_password2:
            return JsonResponse({'code': 400,
                                 'errmsg': '两个密码不一致'})

        # 7.设置数据库中的新密码
        try:
            request.user.set_password(new_password2)

            # 8.保存
            request.user.save()
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '保存密码失败'})

        # 10.清除状态: session + cookie
        logout(request)

        response = JsonResponse({'code': 0,
                             'errmsg': '保存密码成功'})

        response.delete_cookie('username')

        # 9.返回结果json
        return response


class UpdateTitleAddressView(View):

    def put(self, request, address_id):
        '''修改地址标题'''
        # 1.接收json参数
        dict = json.loads(request.body.decode())
        title = dict.get('title')

        # 2.根据address_id获取对应的对象
        try:
            address = Address.objects.get(id=address_id)

            # 3.把该对象的地址改为前端传入的地址
            address.title = title

            # 4.保存结果
            address.save()
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'更新地址标题出错'})

        # 5.返回
        return JsonResponse({'code': 0,
                             'errmsg': 'ok'})


class ChangeDefaultAddressView(View):
    def put(self, request, address_id):
        '''设置默认地址'''

        try:
            # 1.从mysql中根据address_id获取对象
            # address = Address.objects.get(id=address_id)

            # 2.把该对象赋给user中的default_address字段
            # request.user.default_address = address
            request.user.default_address_id = address_id

            # 3.保存
            request.user.save()
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'设置默认地址数据库出错'})

        # 4.返回响应
        return JsonResponse({'code':0,
                             'errmsg':'ok'})


class UpdateDestroyAddressView(View):
    def put(self, request, address_id):
        '''更新某一个指定的地址'''
        # 1.接收参数(json)
        dict = json.loads(request.body.decode())
        receiver = dict.get('receiver')
        province_id = dict.get('province_id')
        city_id = dict.get('city_id')
        district_id = dict.get('district_id')
        place = dict.get('place')
        mobile = dict.get('mobile')
        # 底下的两个字段可以为空:
        phone = dict.get('tel')
        email = dict.get('email')

        # 2.检验参数(整体 + 局部)
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400,
                                 'errmsg': '必传参数有为空的'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': 'mobile格式不正确'})

        if phone:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', phone):
                return JsonResponse({'code': 400,
                                     'errmsg': 'tel格式不正确'})

        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400,
                                     'errmsg': 'email格式不正确'})

        # 3.更新数据库中某一个地址记录 (先查询, 再更新)
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                title=receiver,
                receiver=receiver,
                place=place,
                mobile=mobile,
                phone=phone,
                email=email
            )

            address = Address.objects.get(id=address_id)

        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '更新失败'})

        # 4.拼接json参数, 返回
        dict = {
            'id': address.id,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.phone,
            'email': address.email,
            'title':address.title
        }

        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'address': dict})

    def delete(self, request, address_id):
        '''删除对应的地址'''
        # 1.通过address_id拿取数据库中对应的地址对象
        try:
            address = Address.objects.get(id=address_id)

            # 2.把该地址对象的is_deleted改为true
            address.is_deleted = True

            # 3.保存
            address.save()
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'修改数据库失败'})

        # 4.返回结果
        return JsonResponse({'code':0,
                             'errmsg':'ok'})


class AddressView(View):
    def get(self, request):
        '''返回地址信息'''
        # 1.从mysql中获取当前用户没有删除的地址
        try:
            addresses = Address.objects.filter(user=request.user,
                                               is_delete=False)

            list = []

            # 2.遍历所有地址, 获取每一个地址
            for address in addresses:
                # 3.把每一个地址信息 ---> {} ---> []
                dict = {
                    'id': address.id,
                    'receiver': address.receiver,
                    'province': address.province.name,
                    'city': address.city.name,
                    'district': address.district.name,
                    'province_id': address.province.id,
                    'city_id': address.city.id,
                    'district_id': address.district.id,
                    'place': address.place,
                    'mobile': address.mobile,
                    'tel': address.phone,
                    'email': address.email,
                    'title':address.title
                }

                default_address = request.user.default_address
                if default_address.id == address.id:
                    # address就是默认地址:
                    list.insert(0, dict)
                else:
                    # address不是默认地址:
                    list.append(dict)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':"获取地址失败"})

        # 4.获取默认地址的id
        default_id = request.user.default_address_id

        # 5.拼接参数返回
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'addresses':list,
                             'default_address_id':default_id})


class CreateAddressView(View):
    def post(self, request):
        '''新增地址'''
        # 1.查询数据库中该用户下的所有没有删除的地址个数
        try:
            count = Address.objects.filter(user=request.user,
                                           is_delete=False).count()
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'获取数据库中用户的地址个数出错'})

        # 2.判断该地址个数是否大于等于20, 如果满足, 返回
        if count >= 20:
            return JsonResponse({'code': 400,
                                 'errmsg': '地址超过20个'})

        # 3.如果不满足----> 新增
        # 4.接收参数 json
        dict = json.loads(request.body.decode())
        receiver = dict.get('receiver')
        province_id = dict.get('province_id')
        city_id = dict.get('city_id')
        district_id = dict.get('district_id')
        place = dict.get('place')
        mobile = dict.get('mobile')
        # 底下的两个字段可以为空:
        tel = dict.get('tel')
        email = dict.get('email')

        # 5.校验参数(整体 + 局部)
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400,
                                 'errmsg': '必传参数有为空的'})

        if not re.match(r'', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': 'mobile格式不正确'})

        if tel:
            if not re.match(r'', tel):
                return JsonResponse({'code': 400,
                                     'errmsg': 'tel格式不正确'})

        if email:
            if not re.match(r'', email):
                return JsonResponse({'code': 400,
                                     'errmsg': 'email格式不正确'})

        # 6.往mysql中增加地址
        try:
            address = Address.objects.create(
                user = request.user,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                title = receiver,
                receiver = receiver,
                place = place,
                mobile = mobile,
                phone = tel,
                email = email
            )
            # 7.判断是否有默认地址, 如果没有(第一次增加) 把第一个地址设为默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '增加数据失败'})

        # 8.拼接参数, 返回
        dict = {
            'id': address.id,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.phone,
            'email': address.email,
        }

        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'address':dict})


class VerifyEmailView(View):
    def put(self, request):
        '''验证邮箱'''
        # 1.接收参数
        token = request.GET.get('token')

        # 2.检验参数
        if not token:
            return JsonResponse({'code':400,
                                 'errmsg':'缺少token参数'})

        # 3.解密 token --->  user
        user = User.check_verify_url_token(token)

        # 4.判断 user 是否存在
        if user is None:
            return JsonResponse({'code': 400,
                                 'errmsg': 'token有问题'})

        # 5.更改user的 email_active 为 True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '修改数据库报错'})

        # 6.返回json结果
        return JsonResponse({'code': 0,
                             'errmsg': 'ok'})


class EmailView(View):
    def put(self, request):
        '''修改用户的email'''
        # 1.接收参数
        dict = json.loads(request.body.decode())
        email = dict.get('email')

        # 2.校验参数
        if not email:
            return JsonResponse({'code':400,
                                 'errmsg':'缺少email参数'})

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400,
                                 'errmsg': 'email格式不正确'})


        try:
            # 3.把传入的email修改到数据库
            request.user.email = email

            # 4.保存
            request.user.save()
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '数据库修改失败'})


        verify_url = request.user.generate_verify_url()

        # 补充: 给当前邮箱发送验证邮件:
        send_verify_email.delay(email, verify_url)

        # 5.返回json结果
        return JsonResponse({'code': 0,
                             'errmsg': 'ok'})


class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        '''get请求'''
        # 1. 获取用户
        user = request.user

        # 2. 拼接用户数据
        dict = {
            'username':user.username,
            'mobile':user.mobile,
            'email':user.email,
            'email_active': user.email_active
        }
        # 3. 拼接json字符串, 返回
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'info_data':dict})


class LogoutView(View):
    def delete(self, request):
        '''取消登录功能'''
        # 1.删除session
        logout(request)

        response = JsonResponse({'code':0,
                                 'errmsg':'ok'})

        # 2.清除cookie
        response.delete_cookie('username')

        # 3.返回
        return response


class LoginView(View):
    def post(self, request):
        '''登录的接口'''
        # 1.接收参数(username, password, remembered)
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')

        # 2.检验
        if not all([username, password]):
            return JsonResponse({'code':400,
                                 'errmsg':'缺少必传参数'})

        # 3.认证是否能够登录
        user = authenticate(username=username,
                            password=password)

        # 3.1判断用户是否存在
        if user is None:
            return JsonResponse({'code': 400,
                                 'errmsg': '输入的用户名或密码错误'})

        # 4.状态保持
        login(request,user)

        # 5.判断用户是否勾选了记住状态
        if remembered is True:
            # 6.如果勾选--->保存两周免登陆
            request.session.set_expiry(None)
        else:
            # 7.如果没有勾选---> 浏览器关闭, sessionid立刻过期
            request.session.set_expiry(0)

        # 8.返回状态
        # return JsonResponse({'code': 0,
        #                      'errmsg': 'ok'})
        response =  JsonResponse({'code': 0,
                                  'errmsg': 'ok'})

        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        # 补充内容:购物车的合并
        response = merge_cart_cookie_to_redis(request, response)

        return response


class RegisterView(View):
    def post(self, request):
        '''注册功能接口'''
        # 1.接收参数
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')
        sms_code_client = dict.get('sms_code')

        # 2.校验参数(整体)
        if not all([username, password, password2, mobile, sms_code_client, allow]):
            return JsonResponse({'code':400,
                                 'errmsg':'缺少必传参数'})

        # 3.单个检验: username
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code': 400,
                                 'errmsg': 'username格式不正确'})

        # 4.password
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({'code': 400,
                                 'errmsg': 'password格式不正确'})

        # 5.password 和 password2
        if password != password2:
            return JsonResponse({'code': 400,
                                 'errmsg': '两次输入密码不一致'})

        # 6.mobile
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': 'mobile格式不正确'})

        # 7.allow
        if allow != True:
            return JsonResponse({'code': 400,
                                 'errmsg': '请勾选协议'})

        # 8.链接redis, 获取链接对象
        redis_conn = get_redis_connection('verify_code')

        # 9.利用练级对象, 获取服务端的短信验证码
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        # 10.判断服务端的短信验证码是否存在
        if not sms_code_server:
            return JsonResponse({'code': 400,
                                 'errmsg': '短信验证码过期'})

        # 11.对比前后端的短信验证码
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400,
                                 'errmsg': '输入的短信验证码有误'})

        # 12.把username, password mobile保存到User
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '保存到数据库出错'})

        # 状态保持:
        login(request, user)

        # 13.返回结果(json)
        # return JsonResponse({'code': 0,
        #                      'errmsg': 'ok'})

        response =  JsonResponse({'code': 0,
                                  'errmsg': 'ok'})

        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        # 补充内容:购物车的合并
        response = merge_cart_cookie_to_redis(request, response)

        return response


class MobileCountView(View):

    def get(self, request, mobile):
        '''判断手机号是否重复注册'''
        # 1.查询mobile在mysql中的个数
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'查询数据库出错'})

        # 2.返回结果(json)
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'count':count})


class UsernameCountView(View):
    def get(self, request, username):
        '''判断用户名是否重复'''
        # 1.查询username在数据库中的个数
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'访问数据库失败'})

        # 2.返回结果(json) ---> code & errmsg & count
        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'count': count})


