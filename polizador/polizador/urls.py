from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", auth_views.LoginView.as_view(redirect_authenticated_user=True, redirect_field_name="polizas")),
    path("accounts/", include('django.contrib.auth.urls')),
    path("polizas/", include("carga.urls")),
    #path("api/", include("api.urls")),
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls"))
]
debugpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    # Cambia MEDIA_URL y MEDIA_ROOT si debug=True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debugpatterns
