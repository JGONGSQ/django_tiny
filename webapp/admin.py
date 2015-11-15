from django.contrib import admin
from webapp.models import *

# Register your models here.


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type']
    search_fields = ['user__username', 'type']
admin.site.register(Permission, PermissionAdmin)

