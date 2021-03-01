from django.contrib import admin, messages
from user_manage.models import *
from django.contrib.auth.models import Group
# Register your models here.

from django.contrib import admin
admin.site.site_header = '隧道轮廓自动化测量系统'
admin.site.site_title = '隧道轮廓系统'
# don't display authinfo
# admin.site.unregister(Group)

from django.http import HttpResponse, HttpResponseRedirect

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 最全面的model展示
    list_display = ('username', 'first_name', 'last_name', 'email', 'tel', 'wechat', 'company', 'date_joined',
                    'last_login', 'is_staff', 'is_active', 'is_superuser',)
                    # 'groups', 'user_permissions', 'password', 'create_time', 'update_time'
    search_fields = ('name',)
    list_filter = ('username',)
    # list_editable = ('is_staff', 'is_active')  # 可编辑
    # fk_fields = ('company', ) # 设置显示外键字段

    fieldsets = [
        ('基础信息', {'fields': ['username', 'first_name', 'last_name', 'email', 'tel', 'wechat', 'company']}),
        ('权限设置', {'fields': ['is_staff', 'is_active', 'groups', 'user_permissions', 'password']}),
    ]


    # 增加自定义按钮
    actions = ['to_register']
    def to_register(self, request):
        print("执行注册")
    to_register.short_description = '注册'
    to_register.action_type = 0   # 0=当前页内打开，1=新tab打开，2=浏览器tab打开
    to_register.action_url = '/register'
    to_register.style = 'background:green;color:white;'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contract_number', 'contacts')
    search_fields = ('name',)
    list_filter = ('contract_number',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_company', 'manage_company',  'province', 'city', 'district', 'position')
    search_fields = ('name',)
    list_filter = ('province',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'tunnel_name', 'mileage', 'project')
    search_fields = ('name',)

