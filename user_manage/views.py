from django.shortcuts import render

# Create your views here.
import re
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib import auth, messages
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from user_manage.models import User
from utils.mixin import LoginRequiredMixin


'''
type(request): request的类型
request.environ: request的header详细信息
'''

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
        pass