from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from necesidades.models import Apoyo, Necesidad
from necesidades.routers import NecesidadesRouter

User = get_user_model()


def _perm(app_label, codename):
    return Permission.objects.get(content_type__app_label=app_label, codename=codename)


class RouterTest(SimpleTestCase):
    router = NecesidadesRouter()

    @override_settings(DATABASES={"default": {}, "necesidades": {}})
    def test_con_base_propia(self):
        self.assertEqual(self.router.db_for_write(Necesidad), "necesidades")
        self.assertEqual(self.router.db_for_read(Apoyo), "necesidades")
        self.assertIsNone(self.router.db_for_read(User))
        self.assertTrue(self.router.allow_migrate("necesidades", "necesidades"))
        self.assertFalse(self.router.allow_migrate("default", "necesidades"))
        self.assertFalse(self.router.allow_migrate("necesidades", "auth"))
        self.assertIsNone(self.router.allow_migrate("default", "auth"))

    @override_settings(DATABASES={"default": {}})
    def test_sin_base_propia_usa_default(self):
        self.assertEqual(self.router.db_for_write(Necesidad), "default")
        self.assertTrue(self.router.allow_migrate("default", "necesidades"))


class NecesidadesViewsTest(TestCase):
    databases = "__all__"

    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user("ana", password="x", first_name="Ana", last_name="Pérez")
        cls.beto = User.objects.create_user("beto", password="x")
        cls.gestor = User.objects.create_user("gestor", password="x")
        cls.gestor.user_permissions.add(_perm("necesidades", "gestionar_necesidad"))
        cls.ajeno = User.objects.create_user("ajeno", password="x")

    def _crear(self, **extra):
        datos = {"titulo": "Buscar por DNI", "detalle": "", "ejemplo": "", "modulo": "visor",
                 "tipo": "mejora", "urgencia": 1, "oficina": "Adjudicaciones"}
        datos.update(extra)
        return self.client.post(reverse("necesidades:crear"), datos)

    def test_cualquier_usuario_logueado(self):
        self.assertEqual(self.client.get(reverse("necesidades:lista")).status_code, 302)
        self.client.force_login(self.ajeno)
        self.assertEqual(self.client.get(reverse("necesidades:lista")).status_code, 200)

    def test_crear_guarda_autor(self):
        self.client.force_login(self.ana)
        r = self._crear()
        n = Necesidad.objects.get()
        self.assertRedirects(r, reverse("necesidades:lista") + f"#n{n.pk}", fetch_redirect_response=False)
        self.assertEqual((n.autor_username, n.autor_nombre, n.estado), ("ana", "Ana Pérez", "nueva"))

    def test_titulo_obligatorio(self):
        self.client.force_login(self.ana)
        r = self._crear(titulo="")
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Necesidad.objects.exists())

    def test_solo_autor_o_gestor_editan_y_borran(self):
        self.client.force_login(self.ana)
        self._crear()
        n = Necesidad.objects.get()
        self.client.force_login(self.beto)
        self.assertEqual(self.client.post(reverse("necesidades:borrar", args=[n.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse("necesidades:editar", args=[n.pk])).status_code, 403)
        self.client.force_login(self.gestor)
        self.client.post(reverse("necesidades:borrar", args=[n.pk]))
        self.assertFalse(Necesidad.objects.exists())

    def test_apoyo_alterna_y_no_cuenta_al_autor(self):
        self.client.force_login(self.ana)
        self._crear()
        n = Necesidad.objects.get()
        self.client.post(reverse("necesidades:apoyar", args=[n.pk]))
        self.assertFalse(Apoyo.objects.exists())
        self.client.force_login(self.beto)
        self.client.post(reverse("necesidades:apoyar", args=[n.pk]))
        self.assertEqual(Apoyo.objects.filter(username="beto").count(), 1)
        self.client.post(reverse("necesidades:apoyar", args=[n.pk]))
        self.assertFalse(Apoyo.objects.exists())

    def test_gestionar_requiere_permiso(self):
        self.client.force_login(self.ana)
        self._crear()
        n = Necesidad.objects.get()
        url = reverse("necesidades:gestionar", args=[n.pk])
        datos = {f"g{n.pk}-estado": "hablar", f"g{n.pk}-respuesta": "Lo vemos el martes"}
        self.assertEqual(self.client.post(url, datos).status_code, 403)
        self.client.force_login(self.gestor)
        self.client.post(url, datos)
        n.refresh_from_db()
        self.assertEqual((n.estado, n.respuesta, n.respondido_por), ("hablar", "Lo vemos el martes", "gestor"))

    def test_volver_conserva_solo_filtros_conocidos(self):
        self.client.force_login(self.ana)
        r = self._crear(filtros="modulo=visor&next=https://malo.example")
        self.assertTrue(r["Location"].startswith(reverse("necesidades:lista") + "?modulo=visor#n"))

    def test_resumen_lista_abiertas(self):
        self.client.force_login(self.ana)
        self._crear(titulo="Abierta")
        self._crear(titulo="Cerrada")
        Necesidad.objects.filter(titulo="Cerrada").update(estado="resuelta")
        texto = self.client.get(reverse("necesidades:resumen")).content.decode()
        self.assertIn("Abierta", texto)
        self.assertNotIn("Cerrada", texto)
