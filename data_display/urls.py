'''==================================================
@IDE: PyCharm
@Time : 2020/12/22 11:26 
@Author : wyp
@File : urls.py 
=================================================='''

from django.urls import path, include, re_path
from data_display.views import map_page, get_project_info


app_name = 'data_display'
urlpatterns = [
    path('map_page/', map_page, name='map_page'),
    # path('details/', date_move, name='details'),
    path('get_project_info/', get_project_info, name='data_project'),

]
