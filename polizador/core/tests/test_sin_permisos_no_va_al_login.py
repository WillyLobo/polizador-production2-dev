"""
Un usuario autenticado que NO tiene un permiso tiene que recibir 403, no un
redirect al formulario de login.

Es el modo de falla que aparecio cuando se permitio que cualquiera con cuenta en
el AD entre sin permisos: user_passes_test -- sobre el que esta armado
@permission_required -- redirige a settings.LOGIN_URL cuando el test falla, sin
mirar si la persona ya esta autenticada. El resultado es que alguien que acaba
de entrar aterriza de nuevo en /accounts/login/ como si no hubiera entrado, y si
reenvia ese formulario con el token que quedo en la pagina vieja se lleva un
error de CSRF encima.

52 de los 56 decoradores del proyecto ya pasaban raise_exception=True; estos
tests fijan que los 4 que faltaban no vuelvan a quedarse atras.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()

# Las vistas ruteadas que estaban redirigiendo al login en vez de dar 403.
# (check_resolucion tambien tenia el decorador flojo, pero no esta enganchada a
# ninguna URL, asi que no hay nada que probar desde afuera.)
VISTAS = [
    "/viaticos/ajax/get_agentes/?q=perez",
    "/viaticos/delete-comisionadosolicitud/1/",
    "/viaticos/delete-incorporacion-comisionadosolicitud/1/",
]


class SinPermisosDa403Test(TestCase):
    def setUp(self):
        # Tal como lo deja el alta automatica por LDAP: activo, sin grupos.
        self.user = UserModel.objects.create(username="vperez", ad_username="vperez", is_active=True)
        self.user.set_unusable_password()
        self.user.save()
        self.client.force_login(self.user)

    def test_no_lo_mandan_de_vuelta_al_login(self):
        for url in VISTAS:
            with self.subTest(url=url):
                resp = self.client.get(url)
                assert resp.status_code != 302, f"{url} redirige en vez de dar 403"
                assert "/accounts/login/" not in resp.get("Location", "")

    def test_da_403(self):
        for url in VISTAS:
            with self.subTest(url=url):
                resp = self.client.get(url)
                assert resp.status_code == 403, f"{url} devolvio {resp.status_code}"

    def test_con_el_permiso_pasa(self):
        from django.contrib.auth.models import Permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="secretariador", codename="add_solicitud"))
        self.user = UserModel.objects.get(pk=self.user.pk)  # limpia el cache de permisos
        self.client.force_login(self.user)
        resp = self.client.get("/viaticos/ajax/get_agentes/?q=perez")
        assert resp.status_code != 403
