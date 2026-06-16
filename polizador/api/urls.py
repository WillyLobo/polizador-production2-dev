from django.urls import path
from django.http import JsonResponse
from api.router import api


def version_view(request):
    return JsonResponse({"version": "1.0.0"})


urlpatterns = [
    path("__version__", version_view),
] + api.urls[0]
