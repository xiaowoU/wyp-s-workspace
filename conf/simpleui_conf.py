'''==================================================
@IDE: PyCharm
@Time : 2021/3/2 16:29
@Author : wyp
@File : ss.py
=================================================='''
import os
from configparser import ConfigParser


# 获取相关配置文件
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(BASE_DIR, 'conf', 'conf.ini')
cfg = ConfigParser()
cfg.read(config_file)

# simpleui 设置
# 首页配置
SIMPLEUI_HOME_TITLE = '首页地图导航'
SIMPLEUI_HOME_PAGE = '/data_display/map_page'
# 首页图标,支持element-ui的图标和fontawesome的图标
# SIMPLEUI_HOME_ICON = 'el-icon-date'
# 设置simpleui 点击首页图标跳转的地址
# SIMPLEUI_INDEX = 'https://www.88cto.com'
SIMPLEUI_INDEX = 'http://%s:%s/user_manage/geo/' % (cfg.get('srv', 'host'),
                                                    cfg.get('srv', 'port'))
# 首页显示服务器、python、django、simpleui相关信息
SIMPLEUI_HOME_INFO = False
# 首页显示快速操作
# SIMPLEUI_HOME_QUICK = False
# 首页显示最近动作
# SIMPLEUI_HOME_ACTION = False
# 自定义SIMPLEUI的Logo
# SIMPLEUI_LOGO = 'https://avatars2.githubusercontent.com/u/13655483?s=60&v=4'
# 登录页粒子动画，默认开启，False关闭
# SIMPLEUI_LOGIN_PARTICLES = False
# 让simpleui 不要收集相关信息
SIMPLEUI_ANALYSIS = True
# 自定义simpleui 菜单
SIMPLEUI_CONFIG = {
    'system_keep': True,
    # 'dynamic': True,
    # 'menu_display': ['认证和授权', 'Simpleui', '权限认证', '测试'],
    'menus': [
        {
        'app': 'auth',
        'name': '测量数据展示',
        'icon': 'fas fa-user-shield',
        'models': [
            {
                'name': '数据详情图',
                'icon': 'fa fa-chart-line',
                'url': '/data_display/details_page/'
            },
        ]
    },]
}
# 是否显示默认图标，默认=True
# SIMPLEUI_DEFAULT_ICON = False
# 图标设置，图标参考：
SIMPLEUI_ICON = {
    '系统管理': 'fab fa-apple',
    '员工管理': 'fas fa-user-tie'
}
# 指定simpleui 是否以脱机模式加载静态资源，为True的时候将默认从本地读取所有资源，即使没有联网一样可以。适合内网项目
# 不填该项或者为False的时候，默认从第三方的cdn获取
SIMPLEUI_STATIC_OFFLINE = False
