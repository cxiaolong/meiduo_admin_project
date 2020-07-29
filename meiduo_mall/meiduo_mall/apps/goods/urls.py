from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^list/(?P<category_id>\d+)/skus/$', views.ListView.as_view()),
    re_path(r'^hot/(?P<category_id>\d+)/$', views.HotGoodsView.as_view()),
    # re_path(r'^search/$', views.MySearchView()),
]