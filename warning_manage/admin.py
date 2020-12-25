from django.contrib import admin, messages
from user_manage.models import Warning

# Register your models here.

@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'notify_obj', 'desc', 'project')
    search_fields = ('name', 'project')
    list_filter = ('level',)

