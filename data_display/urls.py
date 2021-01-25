'''==================================================
@IDE: PyCharm
@Time : 2020/12/22 11:26 
@Author : wyp
@File : urls.py 
=================================================='''

from django.urls import path, include, re_path
from data_display.views import map_page, details_page, more_data
from data_display.views import get_project_info, get_details_info


app_name = 'data_display'
urlpatterns = [
    # page
    path('map_page/', map_page, name='map_page'),
    path('details_page/', details_page, name='details_page'),
    path('more_data/', more_data, name='more_data'),

    # api
    path('get_project_info/', get_project_info, name='get_project_info'),
    path('get_details_info/', get_details_info, name='get_details_info'),




]
