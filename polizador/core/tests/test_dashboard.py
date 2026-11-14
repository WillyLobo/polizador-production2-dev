from datetime import datetime, timezone as dt_timezone
from unittest import mock

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from ninja.testing import TestClient

from api.router import api
from core import dashboard_data
from core.models import LoginEvent
from personalizador.models import TipoLicenciaPermiso

UserModel = get_user_model()

# El dashboard cachea Sentry y el estado de la base. Con el caché real (Redis, compartido
# con el servidor de desarrollo) los tests se pisaban entre sí y dejaban datos de la base
# de test a la vista del dashboard de verdad; con Sentry configurado en el .env, además,
# le pegaban a la API real.
aislar_dashboard = override_settings(
    CACHES={**settings.CACHES, "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
    SENTRY_AUTH_TOKEN=None,
    SENTRY_ORG=None,
    SENTRY_PROJECT=None,
)
sentry_configurado = override_settings(SENTRY_AUTH_TOKEN="token", SENTRY_ORG="org", SENTRY_PROJECT="proyecto")


def utc(*args):
    return datetime(*args, tzinfo=dt_timezone.utc)


def respuesta_sentry(issues, headers=None, links=None):
    respuesta = mock.Mock()
    respuesta.json.return_value = issues
    respuesta.headers = headers or {}
    respuesta.links = links or {}
    return respuesta


@aislar_dashboard
class DashboardViewTest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def test_anonymous_redirected_to_login(self):
        resp = self.client.get("/administracion/dashboard/")
        assert resp.status_code == 302

    def test_regular_user_forbidden(self):
        self.client.login(username="plain_user", password="pass1234!")
        resp = self.client.get("/administracion/dashboard/")
        assert resp.status_code == 403

    def test_superuser_allowed(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/dashboard/")
        assert resp.status_code == 200
        self.assertContains(resp, "No configurado")

    @sentry_configurado
    def test_sentry_caido_no_se_muestra_como_no_configurado(self):
        self.client.login(username="admin_user", password="pass1234!")
        with mock.patch("core.dashboard_data.requests.get", side_effect=requests.ConnectionError):
            resp = self.client.get("/administracion/dashboard/")
        self.assertContains(resp, "No se pudo consultar Sentry")
        self.assertNotContains(resp, "No configurado")

    @sentry_configurado
    def test_sentry_muestra_el_total_y_no_el_largo_de_la_pagina(self):
        self.client.login(username="admin_user", password="pass1234!")
        issue = {"title": "Error de prueba", "count": "7", "permalink": "https://sentry.example/1"}
        with mock.patch(
            "core.dashboard_data.requests.get", return_value=respuesta_sentry([issue], headers={"X-Hits": "342"})
        ):
            resp = self.client.get("/administracion/dashboard/")
        self.assertContains(resp, '<p class="card-text fs-3 mb-0">342</p>', html=True)
        self.assertContains(resp, "Error de prueba")


@aislar_dashboard
class DashboardApiTest(TestCase):
    def setUp(self):
        cache.clear()
        self.anon_client = TestClient(api)
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def test_requires_auth(self):
        resp = self.anon_client.get("dashboard/sentry/")
        assert resp.status_code == 401

    def test_regular_user_forbidden(self):
        self.client.login(username="plain_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/sentry/")
        assert resp.status_code == 403

    def test_superuser_allowed(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/sentry/")
        assert resp.status_code == 200

    def test_throughput_unknown_app_label(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/throughput/not-an-app/")
        assert resp.status_code == 404

    def test_throughput_known_app_label(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/throughput/carga/")
        assert resp.status_code == 200
        series = resp.json()["series"]
        assert set(series) == {"Obras", "Certificados", "Fojas de Medición"}
        assert all(len(points) == 12 for points in series.values())

    def test_sentry_not_configured(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/sentry/")
        assert resp.status_code == 200
        assert resp.json()["configured"] is False

    @sentry_configurado
    def test_sentry_error(self):
        self.client.login(username="admin_user", password="pass1234!")
        with mock.patch("core.dashboard_data.requests.get", side_effect=requests.Timeout):
            resp = self.client.get("/v1/api/dashboard/sentry/")
        assert resp.status_code == 200
        assert resp.json() == {
            "configured": True, "error": True, "unresolved_count": None, "truncated": False, "top_issues": [],
        }


@aislar_dashboard
class LoginSummaryTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")

    def login_en(self, momento):
        evento = LoginEvent.objects.create(user=self.user)
        LoginEvent.objects.filter(pk=evento.pk).update(timestamp=momento)  # auto_now_add

    def test_hoy_arranca_en_la_medianoche_local(self):
        # 14/11 01:30 UTC = 13/11 22:30 en Argentina: "hoy" es el 13, desde las 03:00 UTC
        self.login_en(utc(2026, 11, 13, 23, 0))  # 13/11 20:00 local: hoy, aunque en UTC sea "ayer"
        self.login_en(utc(2026, 11, 13, 2, 0))   # 12/11 23:00 local: ayer
        self.login_en(utc(2026, 11, 6, 2, 0))    # 05/11 23:00 local: fuera de los 7 días
        with mock.patch("django.utils.timezone.now", return_value=utc(2026, 11, 14, 1, 30)):
            resumen = dashboard_data.login_summary()
        assert resumen == {"today": 1, "week": 2}


@aislar_dashboard
class RecordThroughputTest(TestCase):
    AHORA = utc(2026, 11, 14, 15, 0)

    def setUp(self):
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.numero = 0

    def alta(self, fecha, usuario=None):
        self.numero += 1
        tipo = TipoLicenciaPermiso(tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre=f"Tipo {self.numero}")
        tipo._history_user = usuario
        tipo.save()
        tipo.tipolicenciapermiso_history.update(history_date=fecha)

    def serie(self):
        with mock.patch("django.utils.timezone.now", return_value=self.AHORA):
            return dict(dashboard_data.record_throughput("personalizador")["Tipos de Licencia"])

    def test_devuelve_los_doce_meses_calendario_aunque_esten_vacios(self):
        serie = self.serie()
        assert list(serie) == [
            "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05",
            "2026-06", "2026-07", "2026-08", "2026-09", "2026-10", "2026-11",
        ]
        assert set(serie.values()) == {0}

    def test_cuenta_por_mes_local_solo_las_altas_hechas_por_usuarios(self):
        self.alta(utc(2026, 11, 3, 12, 0), self.user)
        self.alta(utc(2026, 11, 9, 12, 0), self.user)
        self.alta(utc(2026, 9, 20, 12, 0), self.user)
        # 01/10 02:00 UTC = 30/09 23:00 en Argentina: es de septiembre
        self.alta(utc(2026, 10, 1, 2, 0), self.user)
        # el primer mes de la ventana entra completo, desde su día 1
        self.alta(utc(2025, 12, 1, 12, 0), self.user)
        # sin usuario (carga en bloque, importador): no cuenta
        self.alta(utc(2026, 11, 5, 12, 0))
        # anterior a la ventana
        self.alta(utc(2025, 11, 30, 12, 0), self.user)
        serie = self.serie()
        assert serie["2026-11"] == 2
        assert serie["2026-10"] == 0
        assert serie["2026-09"] == 2
        assert serie["2025-12"] == 1
        assert sum(serie.values()) == 5

    def test_las_modificaciones_no_son_altas(self):
        self.alta(utc(2026, 11, 3, 12, 0), self.user)
        tipo = TipoLicenciaPermiso.objects.get()
        tipo._history_user = self.user
        tipo.tipolicenciapermiso_nombre = "Renombrado"
        tipo.save()
        assert self.serie()["2026-11"] == 1


@aislar_dashboard
class ChangesFeedTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")

    def test_alta_cambio_y_baja_del_mas_nuevo_al_mas_viejo(self):
        tipo = TipoLicenciaPermiso(
            tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre="Razones particulares",
            tipolicenciapermiso_articulo="Art. 1",
        )
        tipo._history_user = self.user
        tipo.save()
        tipo.tipolicenciapermiso_nombre = "Renombrado"
        tipo.save()
        tipo.delete()

        cambios = dashboard_data.changes_feed("personalizador")
        assert [c["tipo"] for c in cambios] == ["Eliminado", "Modificado", "Creado"]
        assert {c["modelo"] for c in cambios} == {"Tipos de Licencia"}
        assert {c["usuario"] for c in cambios} == {self.user}
        assert cambios[-1]["objeto"] == "Art. 1 - Razones particulares (Permiso)"
        assert cambios[0]["objeto"] == "Art. 1 - Renombrado (Permiso)"

    def test_respeta_el_limite(self):
        for numero in range(5):
            TipoLicenciaPermiso.objects.create(tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre=f"Tipo {numero}")
        cambios = dashboard_data.changes_feed("personalizador", limit=3)
        assert [c["objeto"] for c in cambios] == ["None - Tipo 4 (Permiso)", "None - Tipo 3 (Permiso)", "None - Tipo 2 (Permiso)"]


@aislar_dashboard
class SentryHealthTest(TestCase):
    ISSUE = {"title": "ValueError: algo", "count": "12", "permalink": "https://sentry.example/issues/1/"}

    def setUp(self):
        cache.clear()

    def consultar(self, **kwargs):
        with mock.patch("core.dashboard_data.requests.get", **kwargs) as get:
            return dashboard_data.sentry_health(), get

    def test_sin_configurar_no_consulta(self):
        salud, get = self.consultar()
        assert salud is None
        get.assert_not_called()

    @sentry_configurado
    def test_busca_los_ultimos_14_dias_en_el_proyecto(self):
        _, get = self.consultar(return_value=respuesta_sentry([]))
        (url,), kwargs = get.call_args
        assert url == "https://us.sentry.io/api/0/organizations/org/issues/"
        assert kwargs["params"] == {
            "project": "proyecto", "statsPeriod": "14d", "query": "is:unresolved", "sort": "freq", "limit": 100,
        }
        assert kwargs["headers"] == {"Authorization": "Bearer token"}
        assert kwargs["timeout"] == 5

    @sentry_configurado
    def test_el_total_sale_de_x_hits(self):
        salud, _ = self.consultar(return_value=respuesta_sentry([self.ISSUE] * 100, headers={"X-Hits": "342"}))
        assert salud["unresolved_count"] == 342
        assert salud["truncated"] is False
        assert len(salud["top_issues"]) == 5
        assert salud["top_issues"][0] == {"title": "ValueError: algo", "count": "12", "url": "https://sentry.example/issues/1/"}

    @sentry_configurado
    def test_sin_x_hits_y_con_otra_pagina_el_total_es_un_piso(self):
        siguiente = {"next": {"url": "https://us.sentry.io/...", "rel": "next", "results": "true"}}
        salud, _ = self.consultar(return_value=respuesta_sentry([self.ISSUE] * 100, links=siguiente))
        assert salud["unresolved_count"] == 100
        assert salud["truncated"] is True

    @sentry_configurado
    def test_sin_x_hits_y_sin_mas_paginas_el_total_es_exacto(self):
        siguiente = {"next": {"url": "https://us.sentry.io/...", "rel": "next", "results": "false"}}
        salud, _ = self.consultar(return_value=respuesta_sentry([self.ISSUE] * 3, links=siguiente))
        assert salud["unresolved_count"] == 3
        assert salud["truncated"] is False

    @sentry_configurado
    def test_un_fallo_de_red_o_http_es_error(self):
        for fallo in (requests.ConnectionError, requests.Timeout):
            with self.subTest(fallo=fallo):
                cache.clear()
                assert self.consultar(side_effect=fallo)[0] == {"error": True}
        cache.clear()
        respuesta = respuesta_sentry([])
        respuesta.raise_for_status.side_effect = requests.HTTPError("401")
        assert self.consultar(return_value=respuesta)[0] == {"error": True}

    @sentry_configurado
    def test_una_respuesta_con_otra_forma_es_error_y_no_un_500(self):
        for cuerpo in ({"detail": "algo"}, [{"title": "sin permalink"}], None):
            with self.subTest(cuerpo=cuerpo):
                cache.clear()
                assert self.consultar(return_value=respuesta_sentry(cuerpo))[0] == {"error": True}

    @sentry_configurado
    def test_el_resultado_se_cachea(self):
        with mock.patch("core.dashboard_data.requests.get", return_value=respuesta_sentry([self.ISSUE])) as get:
            dashboard_data.sentry_health()
            dashboard_data.sentry_health()
        assert get.call_count == 1
