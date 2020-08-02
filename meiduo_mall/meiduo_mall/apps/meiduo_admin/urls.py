from django.urls import path
from django.urls import re_path
from meiduo_admin.views import skus
from meiduo_admin.views import users
from meiduo_admin.views import statistical
from meiduo_admin.views import permissions

urlpatterns = [
    # 进行url配置
    path('authorizations/', users.AdminAuthView.as_view()),
    path('statistical/day_active/', statistical.UserDayActiveView.as_view()),
    path('statistical/day_orders/', statistical.UserDayOrdersView.as_view()),
    path('statistical/month_increment/', statistical.UserMonthCountView.as_view()),
    path('users/', users.UserInfoView.as_view()),
    # SKU图片管理
    path('skus/images/', skus.SKUImageViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    re_path(r'^skus/images/(?P<pk>\d+)/$', skus.SKUImageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('skus/simple/', skus.SKUSimpleView.as_view()),
    # 权限管理
    # path('permission/perms/', permissions.PermissionViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # })),
    # re_path(r'^permission/perms/(?P<pk>\d+)/$', permissions.PermissionViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'destroy'
    # })),
    path('permission/content_types/', permissions.PermissionViewSet.as_view({
        'get': 'content_types'
    })),
    # path('permission/groups/', permissions.GroupViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create',
    # })),
    # re_path(r'^permission/groups/(?P<pk>\d+)/$', permissions.GroupViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'destroy'
    # })),
    path('permission/simple/', permissions.GroupViewSet.as_view({
        'get': 'simple'
    })),
]

# 路由Router: 图片管理
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('skus/images', skus.SKUImageViewSet, basename='images')
# 路由Router：权限管理
router.register('permission/perms', permissions.PermissionViewSet, basename='perms')
# 路由Router：用户组管理
router.register('permission/groups', permissions.GroupViewSet, basename='groups')
urlpatterns += router.urls































