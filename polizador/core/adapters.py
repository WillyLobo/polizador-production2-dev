"""
Adaptador de allauth para polizador.

Cierra el alta de cuentas por la web. Polizador es una app interna del IPDUV:
las cuentas las crea un administrador desde el panel de Django
(/admin/personalizador/customuser/add/), que es el unico lugar donde ademas se
le asignan los grupos -- sin grupos una cuenta nueva no puede ver nada util, asi
que el alta self-service nunca completaba el trabajo por si sola.

Hasta ahora /accounts/signup/ estaba abierto con los valores por default de
allauth (cuenta ACTIVA, sin verificacion de mail), asi que cualquiera que
llegara al sitio podia crearse un usuario y pasar los login_required. Quedan
como evidencia dos cuentas cuyo username es una direccion personal de correo.

Cerrarlo NO toca a los usuarios existentes: siguen entrando con su usuario y
contrasena como siempre. Lo unico que deja de existir es el alta por la web.
"""
from allauth.account.adapter import DefaultAccountAdapter


class PolizadorAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False
