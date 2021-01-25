from django.apps import AppConfig
import os

app_name = os.path.split(os.path.dirname(__file__))[-1]
default_app_config = '%s.MyConfig' % app_name

class MyConfig(AppConfig):
    name = app_name
    verbose_name = '数据统计'