from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
# Create your views here.
from goods.models import GoodsCategory, SKU
from goods.utils import get_breadcrumb
# 导入:
# from haystack.views import SearchView


# class MySearchView(SearchView):
#     '''重写SearchView类'''
#     def create_response(self):
#         page = self.request.GET.get('page')
#         # 获取搜索结果
#         context = self.get_context()
#         data_list = []
#         for sku in context['page'].object_list:
#             data_list.append({
#                 'id':sku.object.id,
#                 'name':sku.object.name,
#                 'price':sku.object.price,
#                 'default_image_url':sku.object.default_image.url,
#                 'searchkey':context.get('query'),
#                 'page_size':context['page'].paginator.num_pages,
#                 'count':context['page'].paginator.count
#             })
#
#         # 拼接参数, 返回
#         return JsonResponse(data_list, safe=False)


class HotGoodsView(View):
    def get(self, request, category_id):
        '''返回对应category_id的热销商品前两位'''
        # 1.从mysql中获取该类别上架的商品---> 排序(降序) ---> 截取前两个
        try:
            # category1 = GoodsCategory.objects.get(id=category_id)

            skus = SKU.objects.filter(category_id=category_id,
                                      is_launched=True).order_by('-sales')[:2]
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':"获取对应的商品数据失败"})

        list = []
        # 2.遍历两个数据,获取每一个商品对象
        for sku in skus:

            # 3.把商品对象的数据(id&name&image&price) ----> {}  ---> []
            list.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'default_image_url':sku.default_image.url
            })
        # 4.拼接数据,转json, 返回
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'hot_skus':list})


class ListView(View):
    def get(self, request, category_id):
        '''返回列表页中的排过序并且分页的数据'''
        # 1.接收参数
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        ordering = request.GET.get('ordering')

        # 2.根据category_id获取对应的三级类别
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'获取三级类别出错'})

        # 3.TODO:根据三级类别获取面包屑数据(待做)
        breadcrumb = get_breadcrumb(category)

        # 4.获取该三级类别下的所有商品, 根据前端传的数据排序
        try:
            skus = SKU.objects.filter(category=category,
                               is_launched=True).order_by(ordering)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '获取商品出错'})

        # 5.把所有数据进行分页
        paginator = Paginator(skus, page_size)

        # 6.获取 当前页码 的所有商品
        try:
            per_pages_skus = paginator.page(page)
        except EmptyPage as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '获取对应页吗数据出错'})

        # 7.获取所有的总页码
        total_pages = paginator.num_pages

        list = []
        # 8.把当前页码的所有商品遍历, 获取每一个
        for sku in per_pages_skus:

            # 9.把每一个商品的数据(图片&标题&加个&id) ---> {} ===> []
            list.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'default_image_url':sku.default_image.url
            })

        # 10.返回json数据
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'breadcrumb':breadcrumb,
                             'list':list,
                             'count':total_pages})
