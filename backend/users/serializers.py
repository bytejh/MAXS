from rest_framework import serializers
from .models import CustomUser, PermissionGroup, Menu

class MenuSerializer(serializers.ModelSerializer):
    """ 메뉴 직렬화 """
    class Meta:
        model = Menu
        fields = ['id', 'name', 'url']

class PermissionGroupSerializer(serializers.ModelSerializer):
    """권한 그룹 직렬화"""
    menus = MenuSerializer(many=True, read_only=True)


    class Meta:
        model = PermissionGroup
        fields = ['id', 'name', 'description','permissions','menus']

class CustomUserSerializer(serializers.ModelSerializer):
    """사용자 직렬화"""
    permission_group = PermissionGroupSerializer(read_only=True)  # 권한 그룹 읽기 전용

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'phone_number', 'is_active',
            'permission_group',  'created_at'
        ]
        read_only_fields = ['id', 'created_at']

