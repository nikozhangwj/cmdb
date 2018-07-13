# encoding: utf-8

from django.urls import path
from . import views

app_name = 'asset'

urlpatterns = [
    path('',views.index,name='index'),
    path('list/ajax/', views.list_ajax, name='list_ajax'),
    path('resource/ajax/', views.resource_ajax, name='resource_ajax'),
    path('update/ajax/', views.update_ajax, name='update_ajax'),
    path('list_info/ajax/', views.list_info_ajax, name='list_info_ajax')
]
