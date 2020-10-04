from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user', views.github_post, name='github_post'),
    path('user/<str:username>', views.github_get, name='github_get'),
]
