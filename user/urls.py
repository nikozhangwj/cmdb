# encoding: utf-8

from django.urls import path
from . import views


app_name = 'user'


urlpatterns = [
    path('index/',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('delete/',views.delete,name='delete'),
    path('user_info/',views.user_info,name='user_info'),
    path('update/',views.update,name='update'),
    path('create/',views.create,name='create'),
]
