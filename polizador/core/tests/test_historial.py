from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.template import Context, Template
from django.test import RequestFactory, TestCase
from django.urls import reverse

UserModel = get_user_model()


def _url(app_label, model_name, pk):
    return reverse("historial", kwargs={"app_label": app_label, "model_name": model_name, "pk": pk})


class HistorialViewTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")
        self.target = UserModel.objects.create_user(username="target", password="viejo1234!")
        self.url = _url("personalizador", "customuser", self.target.pk)

    def test_nunca_muestra_el_hash_de_la_contrasena(self):
        hash_viejo = self.target.password
        self.target.set_password("nuevo1234!")
        self.target._history_user = self.admin
        self.target.save()
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertContains(response, "(oculto)")
        self.assertNotContains(response, hash_viejo)
        self.assertNotContains(response, self.target.password)

    def test_los_logins_no_generan_entradas(self):
        self.client.login(username="target", password="viejo1234!")
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertNotContains(response, "Modificado")

    def test_sin_permiso_da_403(self):
        self.client.force_login(self.target)
        assert self.client.get(self.url).status_code == 403

    def test_alcanza_con_permiso_de_ver(self):
        self.target.user_permissions.add(Permission.objects.get(codename="view_customuser"))
        self.client.force_login(self.target)
        assert self.client.get(self.url).status_code == 200

    def test_404_para_modelos_inexistentes_sin_historial_o_pk_invalida(self):
        self.client.force_login(self.admin)
        grupo = Group.objects.create(name="g")
        for url in (
            _url("carga", "noexiste", 1),
            _url("auth", "group", grupo.pk),
            _url("personalizador", "customuser", "abc"),
            _url("personalizador", "customuser", 999999),
        ):
            with self.subTest(url=url):
                assert self.client.get(url).status_code == 404

    def test_anonimo_va_al_login(self):
        assert self.client.get(self.url).status_code == 302


class HistorialSidebarTagTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")
        self.plain = UserModel.objects.create_user(username="plain", password="pass1234!")

    def _render(self, user, obj):
        request = RequestFactory().get("/")
        request.user = user
        return Template("{% load historial %}{% historial_sidebar %}").render(
            Context({"request": request, "object": obj})
        )

    def test_se_muestra_si_hay_historial_y_permiso(self):
        assert 'id="historialSidebar"' in self._render(self.admin, self.plain)

    def test_no_se_muestra_sin_permiso(self):
        assert self._render(self.plain, self.admin) == ""

    def test_no_se_muestra_para_modelos_sin_historial_ni_sin_objeto(self):
        assert self._render(self.admin, Group.objects.create(name="g")) == ""
        assert self._render(self.admin, None) == ""


class HistorialM2MTest(TestCase):
    def setUp(self):
        self.admin = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")
        self.target = UserModel.objects.create_user(username="target", password="pass1234!")
        self.editores = Group.objects.create(name="Editores")
        self.otros = Group.objects.create(name="Otros")

    def _cambios(self):
        from core.history import build_timeline, sources_for

        timeline = build_timeline(sources_for(self.target))
        return [
            (e["tipo"], c["campo"], c["antes"], c["despues"])
            for g in timeline["grupos"] for e in g["entradas"] for c in e["cambios"]
        ]

    def test_registra_altas_y_bajas_de_relaciones(self):
        self.target.groups.add(self.editores)
        self.target.groups.add(self.otros)
        self.target.groups.remove(self.editores)

        cambios = self._cambios()

        assert ("Modificado", "grupos", "—", "Editores") in cambios
        assert ("Modificado", "grupos", "Editores", "Editores, Otros") in cambios
        assert ("Modificado", "grupos", "Editores, Otros", "Otros") in cambios

    def test_la_foto_inicial_evita_que_lo_previo_aparezca_como_agregado(self):
        from django.apps import apps
        from core.history import m2m_baseline

        # Como quedaron las relaciones cargadas antes de activar m2m_fields: sin foto.
        self.target.skip_history_when_saving = True
        self.target.groups.add(self.editores)
        del self.target.skip_history_when_saving
        forward, _ = m2m_baseline("personalizador", "customuser", "HistoricalCustomUser", ["groups", "user_permissions"])
        forward(apps, None)

        self.target.groups.add(self.otros)
        cambios = self._cambios()

        assert ("Registro inicial", "grupos", "(sin registro)", "Editores") in cambios
        assert ("Modificado", "grupos", "Editores", "Editores, Otros") in cambios
        assert not any(c[2] == "—" for c in cambios)

    def test_cambio_desde_el_lado_inverso(self):
        self.editores.user_set.add(self.target)

        assert ("Modificado", "grupos", "—", "Editores") in self._cambios()

    def test_clear_desde_el_lado_inverso(self):
        self.target.groups.add(self.editores)
        self.editores.user_set.clear()

        assert ("Modificado", "grupos", "Editores", "—") in self._cambios()
