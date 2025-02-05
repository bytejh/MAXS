from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, PermissionGroupViewSet,  MenuViewSet, CustomUserMenuViewSet

# ViewSet 라우터 설정
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename="user")  # 사용자 API
router.register(r'groups', PermissionGroupViewSet, basename="group")  # 권한 그룹 API
router.register(r'menus', MenuViewSet, basename="menu")  # 메뉴 관리 API 추가
router.register(r'users/(?P<user_id>\d+)/menus', CustomUserMenuViewSet, basename="user-menus")  # 특정 사용자 메뉴 조회 API 추가

# URL 패턴
urlpatterns = [
    path('', include(router.urls)),  # ViewSet 기반 API
]

