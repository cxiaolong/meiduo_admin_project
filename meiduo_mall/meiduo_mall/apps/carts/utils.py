import base64
import pickle
from django_redis import get_redis_connection

def merge_cart_cookie_to_redis(request, response):
    '''合并购物车(cookie----> redis)'''
    # 1.从cookie中获取数据
    cookie_cart = request.COOKIES.get('carts')

    # 2.判断该数据是否存在, 如果不存在, 返回
    if not cookie_cart:
        return response

    # 3.把数据解密 ---> dict
    dict = pickle.loads(base64.b64decode(cookie_cart))

    dict2 = {}
    list1 = []
    list2 = []

    # 4.把dict进行遍历: sku_id + temp_dict
    for sku_id, temp_dict in dict.items():

        # 5.把数据进行分类: {sku_id : count}
        dict2[sku_id] = temp_dict['count']

        # 往set中写入:list1=[sku_id, ...]
        if temp_dict['selected']:
            list1.append(sku_id)
        else:
            # 从set中删除list2=[sku_id, ...]
            list2.append(sku_id)

    # 6.链接redis, 获取链接对象
    redis_conn = get_redis_connection('carts')

    # 7.往hash中写入数据
    redis_conn.hmset('carts_%s' % request.user.id, dict2)

    if list1:
        # 8.判断list1列表是否存在元素,如果有内容,往set中写入
        redis_conn.sadd('selected_%s' % request.user.id, *list1)

    if list2:
        # 9.判断list2列表是否存在元素,如果有内容,从set中删除
        redis_conn.srem('selected_%s' % request.user.id, *list2)

    # 10.删除cookie中的数据
    response.delete_cookie('carts')

    # 11.返回结果
    return response

