from decimal import Decimal

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views import View
from django_redis import get_redis_connection
import json
from goods.models import SKU
from meiduo_mall.utils.views import LoginRequiredMixin
from orders.models import OrderInfo, OrderGoods
from users.models import Address


class OrdersCommitView(View):

    def post(self, request):
        '''提交订单'''
        # 1.接收参数(address_id + pay_method)
        dict = json.loads(request.body.decode())
        address_id = dict.get('address_id')
        pay_method = dict.get('pay_method')

        # 2.总体检验 + 单个检验
        if not all([address_id, pay_method]):
            return JsonResponse({'code':400,
                                 'errmsg':"必传参数有为空的"})
        # 单个检验
        try:
            address = Address.objects.get(id=address_id)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': "address_id有误"})

        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'],
                              OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return JsonResponse({'code': 400,
                                 'errmsg': "address_id有误"})

        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + '%09d' % request.user.id

        # 开启事务:
        with transaction.atomic():
            # 设置保存点:
            save_id = transaction.savepoint()

            # 3.往订单基本表(order_info)中保存数据
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=request.user,
                address=address,
                total_count=0,
                total_amount=Decimal('0.00'),
                freight=Decimal('10.00'),
                pay_method=pay_method,
                status=1 if pay_method == 2 else 2
            )
            # 4.链接redis, 获取链接对象
            redis_conn = get_redis_connection('carts')

            # 5.通过链接对象, 从hash中获取count
            item_dict = redis_conn.hgetall('carts_%s' % request.user.id)

            # 6.通过链接对象, 从set中获取订单中的商品id(sku_id)
            selected_item = redis_conn.smembers('selected_%s' % request.user.id)

            dict = {}
            # 7.把hash: count和set:  sku_id 放到一起(dict)
            for sku_id in selected_item:
                dict[int(sku_id)] = int(item_dict[sku_id])

            # 8.把dict的所有的key取出来: sku_ids
            sku_ids = dict.keys()

            # 9.把sku_ids遍历, 获取每一个sku_id
            for sku_id in sku_ids:

                while True:

                    # 10.通过sku_id获取对应的商品sku
                    sku = SKU.objects.get(id=sku_id)

                    # 11.从dict中取出该id对应的count(卖出的数量)
                    count = dict.get(sku.id)

                    origin_stock = sku.stock
                    origin_sales = sku.sales

                    # 12.判断count(卖出的数量)和库存关系
                    if sku.stock < count:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'code':400,
                                             'errmsg':"库存不足"})

                    # 13.如果库存够, 把sku的库存减少. 销量增加. 保存
                    # sku.stock -= count
                    # sku.sales += count
                    # sku.save()
                    new_stock = origin_stock - count
                    new_sales = origin_sales + count
                    result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock, sales=new_sales)

                    if result == 0:
                        # 没有更新:
                        continue

                    # 14.把sku对应的(spu)的销量增加. 保存
                    sku.spu.sales += count
                    sku.spu.save()

                    # 15.往订单商品表(OrderGoods)中增加数据.
                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=count,
                        price=sku.price
                    )

                    # 16.取出订单, 更新订单的总数量 + 总金额
                    order.total_count += count
                    order.total_amount += (count * sku.price)

                    # 跳出死循环:
                    break

            # 17.更新订单的总金额(运费)
            order.total_amount += order.freight
            # 18.保存订单
            order.save()

            # 撤销保存点(可以不做)
            transaction.savepoint_commit(save_id)

        # 19.删除redis中购物车的相关记录(这些商品从购物车去除)
        redis_conn.hdel('carts_%s' % request.user.id, *selected_item)
        redis_conn.srem('selected_%s' % request.user.id, *selected_item)

        # 20.拼接参数, 返回
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'order_id':order.order_id})




class OrdersSettlementView(LoginRequiredMixin, View):

    def get(self, request):
        '''返回订单结算页面数据'''
        # 1.从地址表中(Address)取出该用户的所有没有删除的地址,得到地址的集合
        try:
            addresses = Address.objects.filter(user=request.user,
                                               is_delete=False)
        except Exception as e:

            addresses = None

        list1 = []
        # 2.遍历该集合, 得到每一个地址 ===> {}  ====> list1=[]
        for address in addresses:
            list1.append({
                "id": address.id,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "receiver": address.receiver,
            })

        # 3.链接redis, 从hash中获取数据(count), 从set中获取数据(sku_id)
        redis_conn = get_redis_connection('carts')
        # hash: item_dict ===> {sku_id:count}
        item_dict = redis_conn.hgetall('carts_%s' % request.user.id)

        # set: selected_item ===> 选中的商品id{sku_id1, sku_id2, ...}
        selected_item = redis_conn.smembers('selected_%s' % request.user.id)

        dict = {}
        # 4.把sku_id + count放入新的dict
        for sku_id in selected_item:
            dict[int(sku_id)] = int(item_dict[sku_id])

        # 5.获取该dict的所有的key值(sku_ids)
        sku_ids = dict.keys()

        # 6.把sku_ids转为skus
        try:
            skus = SKU.objects.filter(id__in=sku_ids)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'获取具体的商品出错'})

        list2 = []
        # 7.遍历所有的skus, 获取每一个sku ====> {} ====> list2=[]
        for sku in skus:
            list2.append({
                "id": sku.id,
                "name": sku.name,
                "default_image_url": sku.default_image.url,
                "count": dict.get(sku.id),
                "price": sku.price,
            })

        # 8.定义一个变量freight用来记录运费
        freight = Decimal('10.00')

        # 9.把上边三部分数据整理到一起context(list1 + list2 + freight )
        context = {
            'addresses':list1,
            'skus':list2,
            'freight':freight
        }

        # 10.拼接参数, 返回json
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'context':context})
