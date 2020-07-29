import base64
import pickle

from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django_redis import get_redis_connection

from goods.models import SKU


class SimpleCartsView(View):

    def get(self, request):
        '''返回简易购物车功能'''
        # 1.判断用户是否登录
        if request.user.is_authenticated:
            # 2.如果用户登录: 链接redis, 获取链接对象
            redis_conn = get_redis_connection('carts')

            # 3.从hash中取出对应的数据
            # item_dict: {sku_id1 : count1, sku_id2:count2, ...}
            item_dict = redis_conn.hgetall('carts_%s' % request.user.id)

            # 4.从set中取出对应的数据 :
            # selected_carts:  {sku_id1, sku_id2, ...}
            selected_carts = redis_conn.smembers('selected_%s' % request.user.id)

            dict = {}
            # 5.把hash + set中有用的数据提取出来放入一个dict中,该dict格式和cookie中dict一样
            for sku_id, count in item_dict.items():
                dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in selected_carts
                }

        else:
            # 6.如果用户未登录: 从cookie中取出保存的数据
            cookie_cart = request.COOKIES.get('carts')

            # 7.判断该数据是否存在, 如果该数据存在 ----> 解密 ----> 得到dict
            if cookie_cart:
                dict = pickle.loads(base64.b64decode(cookie_cart))
            else:
                # 8.如果该数据不存在 -----> 创建新的dict
                dict = {}

        # 9.统一处理:
        # {
        #     sku_id : {
        #         'count':count,
        #         'selected':True/False
        #     }
        # }
        # 10.从dict中获取该dict的所有key值 ===> sku_ids
        sku_ids = dict.keys()

        # 11.把sku_ids转为skus
        try:
            skus = SKU.objects.filter(id__in=sku_ids)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '获取商品数据出错'})

        list = []
        # 12.遍历skus, 获取每一个sku
        for sku in skus:
            # 13.把sku的相关属性存入 ----> {}  ----> []
            list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'count': dict.get(sku.id).get('count'),
            })

        # 14.把[]转为json格式, 返回
        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'cart_skus': list})


class ChoseAllGoods(View):
    def put(self, request):
        '''全选或全不选接口'''
        # 1.接收json参数
        dict = json.loads(request.body.decode())
        selected = dict.get('selected')

        # 2.检验参数
        if selected:
            if not isinstance(selected, bool):
                return JsonResponse({'code':400,
                                     'errmsg':"selected参数有误"})

        # 3.判断用户是否登录
        if request.user.is_authenticated:
            # 4.如果用户登录, 链接redis, 获取链接对象
            redis_conn = get_redis_connection('carts')

            # 5.从hash表中获取对应的dict
            item_dict = redis_conn.hgetall('carts_%s' % request.user.id)

            # 6.从dict中sku_ids取出来
            sku_ids = item_dict.keys()

            # 7.判断前端传入的selected是否为true, 如果为true
            if selected:
                # 8.把sku_ids全部保存到set中
                redis_conn.sadd('selected_%s' % request.user.id, *sku_ids)
            else:
                # 9.如果为false, 把sku_ids值全部从set中删除
                redis_conn.srem('selected_%s' % request.user.id, *sku_ids)
            # 10.返回状态
            return JsonResponse({'code':0,
                                 'errmsg':'ok'})
        else:
            # 11.如果用户未登录, 从cookie中获取数据  -- 解密 ---> dict
            cookie_cart = request.COOKIES.get('carts')

            response = JsonResponse({'code':0,
                                 'errmsg':'ok'})

            if cookie_cart:
                cart_dict = pickle.loads(base64.b64decode(cookie_cart))

                # 12.获取dict中的所有seleted, 用前端传入的selected替换之.
                for sku_id in cart_dict.keys():
                    cart_dict[sku_id]['selected'] = selected

                # 13.把更新后的字典, 加密
                cart_data = base64.b64encode(pickle.dumps(cart_dict)).decode()

                # 14.写入cookie中
                response.set_cookie('carts', cart_data)

            # 15.返回
            return response


class CartsView(View):
    def post(self, request):
        '''增加购物车接口'''
        # 1.接收参数
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        count = dict.get('count')
        selected = dict.get('selected', True)

        # 2.校验参数
        if not all([sku_id, count]):
            return JsonResponse({'code':400,
                                 'errmsg':'必传参数有误'})
        try:
            SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': 'sku_id有误'})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': 'count有误'})
        if selected:
            if not isinstance(selected, bool):
                return JsonResponse({'code': 400,
                                     'errmsg': 'selected有误'})

        # 3.判断用户是否登录
        if request.user.is_authenticated:
            # 4.登录进行的处理  redis (user_id, sku_id, count, selected)

            # 6.链接redis
            redis_conn = get_redis_connection('carts')

            # 7.往redis的hash表中增加数据
            # hash: carts_user_id : {sku_id, count}
            # hincrby: 可以实现累加
            redis_conn.hincrby('carts_%s' % request.user.id,
                               sku_id,
                               count)

            # 8.判断selected是否存在, 如果存在,往set表中增加sku_id
            # set : selected_user_id : {sku_id1, sku_id2, ...}
            if selected:
                redis_conn.sadd('selected_%s' % request.user.id,
                                sku_id)

            # 9.返回响应
            return JsonResponse({'code': 0,
                                 'errmsg': 'ok',
                                 'count': count})
        else:
            # 5.未登录进行的处理
            # 10.从cookie中获取数据
            cookie_cart = request.COOKIES.get('carts')

            # 11.判断该数据是否存在
            if cookie_cart:
                # 12.如果该数据存在 ===> 解密 ===> 老的dict
                cart_dict = pickle.loads(base64.b64decode(cookie_cart))
            else:
                # 13.如果该数据不存在 ---> 创建新的dict
                cart_dict = {}

            # 14.判断前端传入的sku_id是否在dict中
            add_count = count
            if sku_id in cart_dict:
                # 15.如果在, 把前端传入的count和老dict中的count累加, 不存在不累加
                count += cart_dict[sku_id]['count']

            # 16.把前端传入的数据(包含累加过的count)写入dict中
            cart_dict[sku_id] = {
                'count':count,
                'selected':selected
            }
            # 17.把dict加密 ===> 64位的str
            cart_data = base64.b64encode(pickle.dumps(cart_dict)).decode()

            response = JsonResponse({'code':0,
                                     'errmsg':'ok',
                                     'count': add_count})
            # 18.把该str写入cookie
            response.set_cookie('carts', cart_data)

            # 19.返回
            return response

    def get(self, request):
        '''获取购物车数据'''
        # 1.判断用户是否登录
        if request.user.is_authenticated:
            # 2.如果用户登录: 链接redis, 获取链接对象
            redis_conn = get_redis_connection('carts')

            # 3.从hash中取出对应的数据
            # item_dict: {sku_id1 : count1, sku_id2:count2, ...}
            item_dict =redis_conn.hgetall('carts_%s' % request.user.id)

            # 4.从set中取出对应的数据 :
            # selected_carts:  {sku_id1, sku_id2, ...}
            selected_carts = redis_conn.smembers('selected_%s' % request.user.id)

            dict = {}
            # 5.把hash + set中有用的数据提取出来放入一个dict中,该dict格式和cookie中dict一样
            for sku_id, count in item_dict.items():
                dict[int(sku_id)] = {
                    'count':int(count),
                    'selected': sku_id in selected_carts
                }

        else:
            # 6.如果用户未登录: 从cookie中取出保存的数据
            cookie_cart = request.COOKIES.get('carts')

            # 7.判断该数据是否存在, 如果该数据存在 ----> 解密 ----> 得到dict
            if cookie_cart:
                dict = pickle.loads(base64.b64decode(cookie_cart))
            else:
                # 8.如果该数据不存在 -----> 创建新的dict
                dict = {}

        # 9.统一处理:
        # {
        #     sku_id : {
        #         'count':count,
        #         'selected':True/False
        #     }
        # }
        # 10.从dict中获取该dict的所有key值 ===> sku_ids
        sku_ids = dict.keys()

        # 11.把sku_ids转为skus
        try:
            skus = SKU.objects.filter(id__in=sku_ids)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'获取商品数据出错'})

        list = []
        # 12.遍历skus, 获取每一个sku
        for sku in skus:
            # 13.把sku的相关属性存入 ----> {}  ----> []
            list.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'default_image_url':sku.default_image.url,
                'count':dict.get(sku.id).get('count'),
                'amount':sku.price * dict.get(sku.id).get('count'),
                'selected':dict.get(sku.id).get('selected')
            })

        # 14.把[]转为json格式, 返回
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'cart_skus':list})

    def put(self, request):

        '''修改购物车接口'''
        # 1.接收参数
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        count = dict.get('count')
        selected = dict.get('selected', True)

        # 2.检验参数
        if not all([sku_id, count]):
            return JsonResponse({'code': 400,
                                 'errmsg': '必传参数有误'})
        try:
            SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': 'sku_id有误'})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': 'count有误'})
        if selected:
            if not isinstance(selected, bool):
                return JsonResponse({'code': 400,
                                     'errmsg': 'selected有误'})

        # 3.判断用户是否登录
        if request.user.is_authenticated:
            # 4.如果用户登录: 链接redis, 获取链接对象
            redis_conn = get_redis_connection('carts')

            # 5.修改hash数据
            redis_conn.hset('carts_%s' % request.user.id, sku_id, count)

            # 6.判断selected是否是true, 如果是. 把sku_id往set中添加
            if selected:
                redis_conn.sadd('seleted_%s' % request.user.id, sku_id)
            else:
                # 7.如果不是, 把set中的sku_id删除
                redis_conn.srem('seleted_%s' % request.user.id, sku_id)

            dict = {
                'id': sku_id,
                'count': count,
                'selected': selected
            }

            # 8.拼接参数, 返回
            return JsonResponse({'code':0,
                                 'errmsg':'ok',
                                 'cart_sku':dict})
        else:
            # 9.如果用户未登录, 从cookie中获取数据
            cookie_cart = request.COOKIES.get('carts')

            # 10.判断数据是否存在, 如果存在, 解密 得到老dict
            if cookie_cart:
                dict = pickle.loads(base64.b64decode(cookie_cart))
            else:
                # 11.如果不能存在, 创建新的dict
                dict = {}

            # 12.把前端传入的数据,写入dict
            dict[sku_id] = {
                'count':count,
                'selected':selected
            }
            # 13.把dict加密
            cart_data = base64.b64encode(pickle.dumps(dict)).decode()

            temp_dict = {
                'id': sku_id,
                'count': count,
                'selected': selected
            }

            response = JsonResponse({'code':0,
                                 'errmsg':'ok',
                                 'cart_sku':temp_dict})

            # 14.把加密后的数据,写入cookie中
            response.set_cookie('carts', cart_data)

            # 15.拼接参数, 返回
            return response

    def delete(self, request):
        '''删除对应的购物车数据'''
        # 1.接收参数sku_id
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')

        # 2.检验sku_id是否存在
        try:
            SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'sku_id参数有误'})

        # 3.判断用户是否登录
        if request.user.is_authenticated:
            # 4.如果用户登录: 链接redis, 获取链接对象
            redis_conn = get_redis_connection('carts')

            # 5.删除hash中的数据
            redis_conn.hdel('carts_%s' % request.user.id, sku_id)

            # 6.删除set中的数据
            redis_conn.srem('selected_%s' % request.user.id, sku_id)

            # 7.返回
            return JsonResponse({'code':0,
                                 'errmsg':'ok'})
        else:
            # 8.如果用户未登录
            # 9.从cookie中获取数据
            cookie_cart = request.COOKIES.get('carts')

            response = JsonResponse({'code': 0,
                                     'errmsg': 'ok'})

            # 10.判断数据是否存在, 如果存在, 解密, 得到老的dict
            if cookie_cart:
                dict = pickle.loads(base64.b64decode(cookie_cart))

                # 11.判断sku_id是否在老的dict
                if sku_id in dict:
                    # 12.如果在, 删除老的dict中的该记录.
                    del dict[sku_id]

                    # 13.把剩下的老dict加密, 保存到cookie中
                    cart_data = base64.b64encode(pickle.dumps(dict)).decode()

                    response.set_cookie('carts', cart_data)

            # 14.返回数据
            return response
