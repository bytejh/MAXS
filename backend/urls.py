from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf.urls.static import static
from django.conf import settings

def api_root(request):
    """API 루트 안내"""
    return JsonResponse({
        "users": "/api/users/",
        "groups": "/api/groups/",
        "signup": "/api/signup/",
        "menus": "/api/menus/"
    })

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin 페이지
    path('api/', include('users.urls')),  # 사용자 API 연결
    path('api/', api_root, name='api-root'),  # API 루트 경로
    path('', lambda request: JsonResponse({"message": "welcome to datamarketing.kr!"})),  # 기본 메시지
]

# 미디어 파일 경로 (DEBUG 환경에서만 사용)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

