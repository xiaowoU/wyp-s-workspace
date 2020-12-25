'''==================================================
@IDE: PyCharm
@Time : 2020/12/22 11:26 
@Author : wyp
@File : urls.py 
=================================================='''

from django.urls import path, include, re_path
from data_display.views import date_move, home_map


app_name = 'data_display'
urlpatterns = [
    path('details/', date_move, name='details'),
    path('home_map/', home_map, name='home_map'),
]
