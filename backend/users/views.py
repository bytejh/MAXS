from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, PermissionGroup, Menu
from .serializers import CustomUserSerializer, PermissionGroupSerializer, MenuSerializer

class MenuViewSet(ModelViewSet):
    """메뉴 관리 API"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]  # ✅ 로그인한 사용자만 접근 가능

class CustomUserMenuViewSet(ModelViewSet):
    """사용자가 접근 가능한 메뉴 목록 조회 API"""
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """현재 로그인한 사용자가 접근 가능한 메뉴 조회"""
        user = request.user
        if user.permission_group:
            menus = user.permission_group.menus.all()
            serializer = self.get_serializer(menus, many=True)
            return Response(serializer.data)
        return Response([], status=200)

    def retrieve(self, request, *args, **kwargs):
        """특정 사용자가 접근 가능한 메뉴 조회"""
        user = get_object_or_404(CustomUser, pk=kwargs.get("pk"))
        if user.permission_group:
            menus = user.permission_group.menus.all()
            serializer = self.get_serializer(menus, many=True)
            return Response(serializer.data)
        return Response([], status=200)

# 사용자 ViewSet
class CustomUserViewSet(ModelViewSet):
    """ 사용자 관리 API """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        """ 사용자 생성 API (비밀번호 해싱 적용) """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get("password"))  # 비밀번호 해싱 적용
            
            # Permission Group 의 권한을 사용자에게 적용
            if user.permission_group:
                user.user_permissions.set(user.permission_group.permissions.all())

            user.save()
            return JsonResponse({"message": "사용자가 등록되었습니다.", "user": serializer.data}, status=201)
        return JsonResponse(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        """ 사용자 수정 시 비밀번호 변경 가능하도록 처리 """
        user = self.get_object()
        password = request.data.get("password")

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            if password:
                user.set_password(password)
                user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        """ 사용자 삭제 API """
        user = self.get_object()
        user.delete()
        return JsonResponse({"message": "사용자가 삭제되었습니다."}, status=204)

# 권한 그룹 ViewSet
class PermissionGroupViewSet(ModelViewSet):
    """ 권한 그룹 관리 API """
    queryset = PermissionGroup.objects.all()
    serializer_class = PermissionGroupSerializer

# 회원가입 API
@csrf_exempt
def signup_request(request):
    """ 회원가입 API (비밀번호 해싱 적용) """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone')

            # 필수 항목 확인
            if not username or not email or not password:
                return JsonResponse({"error": "필수 항목 누락"}, status=400)

            # 중복 확인
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({"error": "이미 존재하는 사용자 이름입니다."}, status=400)
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"error": "이미 존재하는 이메일 주소입니다."}, status=400)

            # 사용자 생성 (비밀번호 해싱 추가)
            user = CustomUser.objects.create(username=username, email=email, phone_number=phone)
            user.set_password(password)  # 비밀번호 해싱 적용
            user.save()

            return JsonResponse({"message": "회원가입 성공"}, status=201)
        except Exception as e:
            return JsonResponse({"error": f"회원가입 중 오류가 발생했습니다: {str(e)}"}, status=500)
    return JsonResponse({"error": "허용되지 않은 메서드입니다."}, status=405)

