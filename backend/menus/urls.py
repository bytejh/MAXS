from django.urls import path
from .views import MenuListView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # 기본화면 API
    path('menu-list/', MenuListView.as_view(), name='menu-list'),
]

