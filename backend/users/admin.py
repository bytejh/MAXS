from django.contrib import admin
from django.contrib.auth.models import Group   # Django 기본 Group
from .models import CustomUser, PermissionGroup, Menu

# Django 기본 Group 숨기기
admin.site.unregister(Group) # Django 기본 Group 숨기기

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    search_fields = ('name', 'url')

@admin.register(PermissionGroup)
class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions','menus')
    fields = ('name','description','permissions','menus')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'permission_group',  'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'permission_group')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'is_active', 'permission_group')}),
    )

