from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class StandardResultPagination(PageNumberPagination):
    # 指定分页的默认页容量
    page_size = 5
    # 指定获取分页数据时，页容量参数的名称
    # 注意：下面这个属性不要写成：page_query_param
    page_size_query_param = 'pagesize'
    # 指定分页时的最大页容量
    max_page_size = 10

    def get_paginated_response(self, data):
        """重写父类方法,自定义分页响应数据格式"""
        return Response(OrderedDict([
            ('counts', self.page.paginator.count),
            ('lists', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ]))























