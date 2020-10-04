from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<str:username>', views.github_user, name='github_user'),
]
