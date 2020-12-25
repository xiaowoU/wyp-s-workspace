
from django.urls import path, include, re_path
# from user_manage.views import get_bar, get_map, get_line
from user_manage.views import GetChartView


app_name = 'user_manage'
urlpatterns = [
    # path('bar/', GetChartView.get_bar, name='bar'),
    # path('map/', get_map, name='map'),
    # path('line/', get_line, name='line'),
    re_path('^(?P<chart>.*)/$', GetChartView.as_view(), name='chart'),   # bar map line
]
