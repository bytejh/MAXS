from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group  # Django 기본 Group
from .models import CustomUser, PermissionGroup, Menu

# Django 기본 Group 숨기기
admin.site.unregister(Group)


# ✅ User 수정 시 사용할 Form 추가 (비밀번호 변경 가능)
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "is_active", "is_staff", "permission_group")


# ✅ UserAdmin 설정 (Admin에서 Password 필드 표시)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm  # 수정 시 사용할 폼 설정
    list_display = ("username", "email", "permission_group", "is_active", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("is_active", "permission_group", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "email", "phone_number", "is_active", "is_staff", "permission_group")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone_number", "password1", "password2"),
        }),
    )

    def save_model(self, request, obj, form, change):
        """ Change 화면에서 저장할 때 Permission 자동 적용 """

        # ✅ 신규 생성된 User의 기본값 설정
        if not change:
            obj.is_staff = False
            obj.is_active = False

        # ✅ Change 화면에서 `is_staff`, `is_active` 변경 시 Permission 적용
        if change and obj.permission_group:
            obj.user_permissions.set(obj.permission_group.permissions.all())

        obj.save()


# ✅ Admin 등록 (`@admin.register()` 대신 `admin.site.register()` 사용)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    search_fields = ('name', 'url')


class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions', 'menus')
    fields = ('name', 'description', 'permissions', 'menus')


admin.site.register(Menu, MenuAdmin)
admin.site.register(PermissionGroup, PermissionGroupAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

