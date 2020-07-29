from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
# Create your views here.
from areas.models import Area
from django.core.cache import cache



class SubAreaView(View):
    
    def get(self, request, pk):
        '''请求市区数据'''
        dict = cache.get('dict_' + pk)

        if not dict:

            # 1.从mysql中获取市数据
            try:
                sub_model_list = Area.objects.filter(parent=pk)

                # 2.从mysql中获取pk对应的省份数据
                parent_model = Area.objects.get(id=pk)

                list = []
                # 3.遍历市的数据, 获取每一个市 ---> {} ---> []
                for sub_model in sub_model_list:
                    list.append({
                        'id':sub_model.id,
                        'name':sub_model.name
                    })

                # 4.拼接省份数据
                dict = {
                    'id':parent_model.id,
                    'name':parent_model.name,
                    'subs':list
                }

                # cache.set('dict_%s' % pk, dict, 3600)
                cache.set('dict_' + pk, dict, 3600)

            except Exception as e:
                return JsonResponse({'code':400,
                                     'errmsg':"获取数据库数据失败"})

        # 5.拼接json数据, 返回
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'sub_data':dict})



class ProvinceView(View):

    def get(self, request):
        '''返回省份数据'''
        # 0. 读取缓存中的数据:
        province_list = cache.get('province_list')

        if not province_list:
            # 1.从mysql中获取所有的省份数据
            try:
                province_model_list = Area.objects.filter(parent__isnull=True)

                province_list = []

                # 2.遍历这些省份数据, 获取每一个省份对象
                for province_model in province_model_list:

                    # 3.把省份对象的信息 ---> {} ---> []
                    province_list.append({
                        'id':province_model.id,
                        'name':province_model.name
                    })

                cache.set('province_list', province_list, 3600)
            except Exception as e:
                return JsonResponse({'code':400,
                                     'errmsg':"从mysql中获取省份数据出错"})

        # 4.拼接参数, 转为json, 返回
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'province_list':province_list})
