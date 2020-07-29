from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^orders/settlement/$', views.OrdersSettlementView.as_view()),
    re_path(r'^orders/commit/$', views.OrdersCommitView.as_view()),
]