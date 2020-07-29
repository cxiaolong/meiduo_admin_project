from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^qq/authorization/$', views.OAuthURLView.as_view()),
    re_path(r'^oauth_callback/$', views.OAuthUserView.as_view()),
]