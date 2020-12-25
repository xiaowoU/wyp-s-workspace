from django.contrib import admin, messages
from user_manage.models import OutLine, Result

# Register your models here.

@admin.register(OutLine)
class OutLineAdmin(admin.ModelAdmin):
    list_display = ('device_sn', 'angle', 'range', 'turns_flag', 'times', 'section')
    search_fields = ('device_sn',)
    list_filter = ('device_sn',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('device_sn', 'convergence', 'sedimentation', 'timestamp', 'section')
    search_fields = ('device_sn',)
    list_filter = ('device_sn',)


