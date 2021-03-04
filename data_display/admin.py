from django.contrib import admin, messages
from user_manage.models import CollectRaw, Result, UnifyDataRaw

# Register your models here.

@admin.register(CollectRaw)
class CollectRawAdmin(admin.ModelAdmin):
    list_display = ('device_sn', 'scan_time', 'scan_points', 'start_angle', 'step', 'angle', 'range', 'turns_flag', 'times', 'timestamp')
    search_fields = ('device_sn',)
    list_filter = ('device_sn',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('device_sn', 'convergence', 'sedimentation', 'timestamp',)
    search_fields = ('device_sn',)
    list_filter = ('device_sn',)


@admin.register(UnifyDataRaw)
class UnifyDataRawAdmin(admin.ModelAdmin):
    list_display = ('device_sn', 'meas_time', 'index', 'value')
    search_fields = ('device_sn',)
    list_filter = ('device_sn',)
