from django.contrib import admin, messages
from user_manage.models import *
from django.contrib.auth.models import Group
# Register your models here.

from django.contrib import admin
admin.site.site_header = '隧道轮廓自动化测量系统'
admin.site.site_title = '隧道轮廓系统'
# don't display authinfo
admin.site.unregister(Group)

from django.http import HttpResponse, HttpResponseRedirect

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'real_name', 'date_joined', 'email', 'company')
    search_fields = ('name',)
    list_filter = ('username',)
    list_editable = ('real_name',)
    # fk_fields 设置显示外键字段
    fk_fields = ('company', )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contract_number', 'contacts')
    search_fields = ('name',)
    list_filter = ('contract_number',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'city', 'district')
    search_fields = ('name',)
    list_filter = ('province',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_sn', 'section', 'firmware_version', 'type', 'model', 'ip', 'mac')
    search_fields = ('device_sn', 'firmware_version')
    list_filter = ('type',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'mileage')
    search_fields = ('name',)
    list_filter = ('name',)

