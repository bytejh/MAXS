from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Menu, MenuGroup

class MenuListView(APIView):
    def get(self, request):
        menus = Menu.objects.filter(sta_type='0')  # Active menus only
        return Response([
            {
                "id": m.id,
                "name": m.name,
                "group": m.group.name,
                "url": m.url
            } for m in menus
        ])

class HomeView(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the Main Homepage!",
            "status": "success"
        })
