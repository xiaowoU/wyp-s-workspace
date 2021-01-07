from django.shortcuts import render

# Create your views here.
import re
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib import auth, messages
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from user_manage.models import User, Project
from user_manage.formAuth import RegForm, LoginForm
from utils.mixin import LoginRequiredMixin
from db.proxy import ReadGeoInfo, ReadDataInfo

from pyecharts import options as opts
from pyecharts.charts import Bar, Map, Line



'''
type(request): request的类型
request.environ: request的header详细信息
'''

# /test
def test(request):
    # d2 = datetime.datetime.strptime(j, '%Y-%m-%d %H:%M:%S')
    return HttpResponse("TEST")


# /index
def index(request):
    return render(request, 'base.html')

# /register
class RegisterView(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        # print(type(request))
        # print(request.environ)
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 进行业务处理: 用户注册
        user = User.objects.create_user(username, email, password)
        # todo: use system
        user.is_staff = 1
        user.save()
        # return HttpResponseRedirect(reverse('login'))
        return HttpResponseRedirect("/admin/login/")

# /login
class LoginView(View):
    '''登录'''
    def get(self, request):
        # print("Login get=================")
        '''显示登录页面'''
        # 判断是否记住了用户名
        username = ''
        checked = ''
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        # print("User: %s, Checked: %s" % (username, checked))
        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        # print(type(request))
        # print(request.environ)
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})
        # 业务处理:登录校验
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确, 记录用户的登录状态
            auth.login(request, user)
            # 获取登录后要跳转得地址，默认为首页
            next_url = request.GET.get('next', reverse('index'))
            response = HttpResponseRedirect(next_url)
            # # 判断是否需要记住用户名
            # remember = request.POST.get('remember')
            # if remember == 'on':
            #     # 记住用户名
            #     response.set_cookie('username', username, max_age=7*24*3600)
            # else:
            #     response.delete_cookie('username')
            # 返回response
            return response
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})

# /logout
class LogoutView(LoginRequiredMixin, View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        auth.logout(request)
        # 跳转
        return HttpResponseRedirect(reverse('login'))


'''
================分割线===================
'''
class GetChartView(LoginRequiredMixin, View):
    def get(self, request, chart):
        # print('============%s=============' % chart)
        dct = {'bar': self.get_bar,
               'line': self.get_line,
               'geo': self.get_geo}
        if chart not in dct:
            return HttpResponse("Error URL!!!!")
        else:
            # return HttpResponse(bar.render_embed())
            return HttpResponse(dct[chart]().render_embed())

    def get_bar(self) -> Bar:
        bar = (
            Bar()
                .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
                .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
                .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
                .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
        )
        return bar

    @classmethod
    # todo: param为device_sn,一张图表示一个设备情况
    def get_line(self):
        lineinfo = ReadDataInfo()
        line_chart = lineinfo.generate_line("sn_001")
        return line_chart


    # /user_manage/line
    # @decorators.permission_required
    @classmethod
    def get_geo(self):
        geoinfo = ReadGeoInfo()
        geo_map = geoinfo.generate_geo()
        return geo_map

