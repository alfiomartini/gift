from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index_adv', views.index_adv, name='index_adv'),
    path('user/post', views.user_post, name='post_user'),
    path('user/get/<str:username>', views.user_get, name='get_user'),
    path('user/<str:username>/<str:sort>',
         views.user_render, name='user_render'),
    path('user/js/<str:username>', views.user_repos, name='user_repos'),
    path('users/get/<str:query>/<str:sort>',
         views.search_users, name='search_users'),
    path('repos/get/<str:query>/<str:sort>',
         views.search_repos, name='search_repos'),
    path('charts/<str:category>', views.charts, name='charts'),
    path('readme', views.readme, name='readme'),
    path('apply_adv', views.apply_adv, name='apply_adv'),
    path('reset_adv', views.reset_adv, name='reset_adv'),

]
