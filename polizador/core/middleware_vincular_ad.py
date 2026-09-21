"""
Empuja a los usuarios sin cuenta de red vinculada hacia la pagina de vinculacion
(core/views_vincular_ad.py).

Deliberadamente acotado a la navegacion normal: solo GET de paginas HTML. Un
redirect sobre una llamada de la API o sobre una peticion AJAX no lo ve nadie y
rompe la funcionalidad en silencio, asi que esas pasan de largo y el usuario ve
el pedido la proxima vez que abra una pagina.

Se apaga con AD_VINCULACION_OBLIGATORIA = False (por ejemplo antes de anunciarlo,
o si el AD queda fuera de servicio un rato largo).
"""
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

# Prefijos que nunca se interceptan:
#   /accounts/  -- login y logout; redirigir el logout dejaria a la gente sin
#                  forma de salir mientras no vincule
#   /admin/     -- para que un administrador pueda arreglar las cosas
#   /v1/api/, /select2/  -- respuestas JSON
#   /static/, /media/    -- archivos
EXENTOS = ("/accounts/", "/admin/", "/v1/api/", "/select2/", "/static/", "/media/")


class VincularADMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._hay_que_pedirlo(request):
            return redirect(reverse("vincular_ad"))
        return self.get_response(request)

    def _hay_que_pedirlo(self, request):
        if not getattr(settings, "AD_VINCULACION_OBLIGATORIA", False):
            return False
        if request.method != "GET":
            return False
        usuario = getattr(request, "user", None)
        if usuario is None or not usuario.is_authenticated:
            return False
        if usuario.ad_username or usuario.ad_sin_cuenta_red:
            return False
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return False
        if "text/html" not in request.headers.get("accept", "text/html"):
            return False
        ruta = request.path
        if ruta.startswith(EXENTOS) or ruta == reverse("vincular_ad"):
            return False
        return True
