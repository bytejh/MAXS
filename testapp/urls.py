from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 'index'는 기본 경로의 뷰 함수
]

