# encoding: utf-8

from django.urls import path
from . import views


app_name = 'user'


urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('delete/',views.delete,name='delete'),
    path('user_info/',views.user_info,name='user_info'),
    path('update/',views.update,name='update'),
    path('create/',views.create,name='create'),
    path('change_password/',views.change_password,name='change_password'),
    path('create/ajax',views.create_ajax,name='create_ajax'),
    path('delete/ajax',views.delete_ajax,name='delete_ajax'),
    path('change_password_ajax/',views.change_password_ajax,name='change_password_ajax'),
    path('list/ajax',views.list_ajax,name='list_ajax')

]
