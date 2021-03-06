from django.contrib import admin
from django.urls import path, re_path, include
from . import views_get
from . import views_post
urlpatterns = [
    re_path(r'post/', views_post.post, name='post'),
    path('check/', views_get.signin, name='signin'),
    path('notify/', views_get.notify, name='notify'),
]