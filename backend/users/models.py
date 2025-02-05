from django.contrib.auth.models import AbstractUser, Permission
from django.db import models

class Menu(models.Model):
    """메뉴 정보 테이블"""
    name = models.CharField(max_length=50, unique=True, verbose_name="메뉴 이름")
    url = models.CharField(max_length=200, unique=True, verbose_name="메뉴 URL")

    def __str__(self):
        return self.name

class PermissionGroup(models.Model):
    """사용자 권한 그룹"""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name="권한 그룹 이름")
    description = models.TextField(blank=True, null=True, verbose_name="설명")
    permissions = models.ManyToManyField(Permission, blank=True, related_name="permission_groups")
    menus = models.ManyToManyField("users.Menu", blank=True, related_name="permission_groups") 

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """사용자 모델 확장"""
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="전화번호")
    permission_group = models.ForeignKey(
        "users.PermissionGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="권한 그룹"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 날짜")
    
    class Meta:
        permissions = []
   
    def has_access_to_menu(self,menu):
        """ 사용자가 특정 메뉴에 접근할 수 있는지 확인 """
        if self.permission_group:
            return self.permission_group.menus.filter(id=menu.id).exists()
        return False

    def save(self, *args, **kwargs):
        """Permission Group을 기반으로 Permissions 자동 설정"""
        super().save(*args, **kwargs)
        if self.permission_group:
            self.user_permissions.set(self.permission_group.permissions.all())  # 권한 자동 설정


    def __str__(self):
        return self.username

