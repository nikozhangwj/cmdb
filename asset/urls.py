# encoding: utf-8

from django.urls import path
from . import views

app_name = 'asset'

urlpatterns = [
    path('',views.index,name='index'),
    path('list/ajax/', views.list_ajax, name='list_ajax'),
]
