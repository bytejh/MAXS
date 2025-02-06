from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group   # Django 기본 Group
from .models import CustomUser, PermissionGroup, Menu

# Django 기본 Group 숨기기
admin.site.unregister(Group)

# ✅ User 수정 시 사용할 Form 추가 (비밀번호 변경 가능)
class CustomUserChangeForm(forms.ModelForm):
    """ User 수정 시 Password 필드 추가 """
    password = forms.CharField(
        label="새 비밀번호",
        widget=forms.PasswordInput,
        required=False,  # 필수 입력 아님
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "is_active", "permission_group", "password")

    def save(self, commit=True):
        """ 비밀번호가 입력된 경우 set_password() 적용 """
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# ✅ UserAdmin 설정 (Admin에서 Password 필드 표시)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm  # 수정 시 사용할 폼 설정
    list_display = ("username", "email", "permission_group", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_active", "permission_group")

    fieldsets = (
        (None, {"fields": ("username", "email", "phone_number", "is_active", "permission_group")}),
        ("비밀번호 변경", {"fields": ("password",)}),  # ✅ Password 필드 추가
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone_number", "password1", "password2"),
        }),
    )

    def save_model(self, request, obj, form, change):
        """ 비밀번호가 변경되면 set_password() 적용 """
        if "password" in form.cleaned_data:
            obj.set_password(form.cleaned_data["password"])
        obj.save()

# ✅ Admin 등록 (`@admin.register()` 대신 `admin.site.register()` 사용)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    search_fields = ('name', 'url')

class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions','menus')
    fields = ('name','description','permissions','menus')

admin.site.register(Menu, MenuAdmin)
admin.site.register(PermissionGroup, PermissionGroupAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

