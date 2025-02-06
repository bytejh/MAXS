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
    permission_group = PermissionGroupSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "email", "phone_number", "is_active",
            "permission_group", "password", "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        """User 생성 시 비밀번호 암호화"""
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """User 수정 시 비밀번호 변경 가능하도록 설정"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

