from django.contrib import admin
from user_manage.models import Param
# Register your models here.

@admin.register(Param)
class ParamAdmin(admin.ModelAdmin):
    list_display = ('device_sn', 'scan_resolution', 'start_angle', 'end_angle', 're_times', 'cycle')    # 'turns_flag',
    search_fields = ('device_sn', 'turns_flag')
    list_filter = ('turns_flag',)

