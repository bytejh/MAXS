from django.http import JsonResponse

def group_view(request):
    return JsonResponse({"message": "Group API works"})

