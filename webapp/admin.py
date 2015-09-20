from django.contrib import admin
from webapp.models import *

# Register your models here.


class UserPermissionTypeAdmin(admin.ModelAdmin):
    list_display = ['user', 'type']
    search_fields = ['user__username', 'type']
admin.site.register(UserPermissionType, UserPermissionTypeAdmin)

