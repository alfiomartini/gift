from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/post', views.user_post, name='post_user'),
    path('user/get/<str:username>', views.user_get, name='get_user'),
    path('user/<str:username>', views.user_render, name='user_render'),
]
