from datetime import date, datetime, timezone as dt_timezone
from decimal import Decimal
from unittest import mock

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.apps import apps
from django.db import DatabaseError, connection
from django.test.utils import CaptureQueriesContext
from django.contrib.auth.signals import user_logged_in
from django.test import Client, RequestFactory, TestCase, override_settings
from ninja.testing import TestClient

from api.router import api
from carga.models import (
    CertificadoRubro, Empresa, Obra, PlanDeTrabajos, PlanDeTrabajosEtapa, PlanDeTrabajosRubro, Programa,
)
from core import dashboard_data
from core.history import history_manager
from core.models import LoginEvent
from personalizador.models import GeneroAgente, TipoLicenciaPermiso

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
    def test_la_pagina_no_espera_a_sentry(self):
        # el tile lo completa el navegador pidiéndole el dato a la API
        self.client.login(username="admin_user", password="pass1234!")
        with mock.patch("core.dashboard_data.requests.get") as get:
            resp = self.client.get("/administracion/dashboard/")
        get.assert_not_called()
        self.assertContains(resp, 'getJSON("/v1/api/dashboard/sentry/")')
        self.assertContains(resp, 'data-url="/v1/api/dashboard/throughput/carga/"')

    def test_una_pestana_por_app_con_historial_y_nada_se_calcula_al_abrir(self):
        self.client.login(username="admin_user", password="pass1234!")
        with mock.patch("core.dashboard_data.changes_feed") as feed, mock.patch("core.dashboard_data.record_throughput") as altas:
            resp = self.client.get("/administracion/dashboard/")
        feed.assert_not_called()
        altas.assert_not_called()
        pestanas = [app["display"] for app in resp.context["apps"]]
        assert pestanas[:3] == ["Obras", "Viáticos", "Personal"]
        assert len(pestanas) == len(dashboard_data.tracked_apps())
        # solo la primera pestaña se pide al cargar; las otras, al abrirlas
        self.assertContains(resp, 'hx-get="/administracion/dashboard/cambios/carga/"')
        self.assertContains(resp, 'hx-trigger="load"', count=1)
        self.assertContains(resp, 'hx-trigger="shown.bs.tab from:#tab-personalizador-btn once"')

    def test_una_seccion_que_falla_no_tira_la_pagina(self):
        self.client.login(username="admin_user", password="pass1234!")

        def consulta_rota(limit):
            # como pg_stat_statements creada pero sin cargar: el SELECT revienta
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tabla_que_no_existe")

        with mock.patch("core.dashboard_data._fetch_db_performance", consulta_rota), self.assertLogs("core.views", "ERROR"):
            resp = self.client.get("/administracion/dashboard/")
        assert resp.status_code == 200
        assert resp.context["db_performance"] == {"error": True}
        self.assertContains(resp, "No disponible", count=1)
        # las secciones que se calculan después siguen andando: el error de SQL no dejó
        # abortada la transacción
        assert "size" in resp.context["db_health"] or "size" in dashboard_data.db_health()

    def test_todas_las_secciones_pueden_fallar_a_la_vez(self):
        self.client.login(username="admin_user", password="pass1234!")
        rota = mock.Mock(side_effect=RuntimeError("roto"))
        with (
            mock.patch.multiple(
                "core.dashboard_data", login_summary=rota, recent_logins=rota, db_health=rota, db_performance=rota,
            ),
            self.assertLogs("core.views", "ERROR"),
        ):
            resp = self.client.get("/administracion/dashboard/")
        assert resp.status_code == 200
        # 2 KPIs de logins + últimos logins + base + consultas
        self.assertContains(resp, "No disponible", count=5)

    def test_estado_de_la_base(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/dashboard/")
        salud = resp.context["db_health"]
        assert salud["active_connections"] >= 1  # al menos la que hace la consulta
        assert salud["total_connections"] >= salud["active_connections"]
        self.assertContains(resp, "Conexiones (activas / total)")
        self.assertNotContains(resp, "None%")

    def test_cache_hit_ratio_sin_datos(self):
        self.client.login(username="admin_user", password="pass1234!")
        salud = {**dashboard_data._fetch_db_health(), "cache_hit_ratio": None}
        with mock.patch("core.dashboard_data.db_health", return_value=salud):
            resp = self.client.get("/administracion/dashboard/")
        self.assertNotContains(resp, "None%")


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
        assert resp.json() == {"series": {}}  # nadie creó nada todavía

    def test_throughput_de_una_app_sin_historial(self):
        self.client.login(username="admin_user", password="pass1234!")
        assert self.client.get("/v1/api/dashboard/throughput/core/").status_code == 404

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

    def altas(self, **kwargs):
        with mock.patch("django.utils.timezone.now", return_value=self.AHORA):
            return dashboard_data.record_throughput("personalizador", **kwargs)

    def serie(self):
        return dict(self.altas()["Tipos de Licencias/Permisos"])

    def test_devuelve_los_doce_meses_calendario_aunque_esten_vacios(self):
        self.alta(utc(2026, 11, 3, 12, 0), self.user)
        serie = self.serie()
        assert list(serie) == [
            "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05",
            "2026-06", "2026-07", "2026-08", "2026-09", "2026-10", "2026-11",
        ]
        assert sum(serie.values()) == serie["2026-11"] == 1

    def test_un_modelo_sin_altas_de_usuarios_no_aparece(self):
        self.alta(utc(2026, 11, 3, 12, 0))  # sin usuario
        assert self.altas() == {}

    def test_los_modelos_con_mas_altas_van_aparte_y_el_resto_en_otros(self):
        for _ in range(3):
            self.alta(utc(2026, 11, 3, 12, 0), self.user)
        for numero in range(2):
            genero = GeneroAgente(generoagente_nombre=f"Género {numero}")
            genero._history_user = self.user
            genero.save()
            history_manager(GeneroAgente).filter(id=genero.pk).update(history_date=utc(2026, 10, 3, 12, 0))
        todos = self.altas()
        assert list(todos) == ["Tipos de Licencias/Permisos", "Géneros"]  # de más a menos altas
        agrupado = self.altas(top=1)
        assert list(agrupado) == ["Tipos de Licencias/Permisos", "Otros"]
        assert dict(agrupado["Otros"])["2026-10"] == 2
        assert sum(total for _, total in agrupado["Otros"]) == 2

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
class TrackedAppsTest(TestCase):
    def test_incluye_todo_modelo_con_historial_sin_lista_a_mano(self):
        esperados = {
            model for model in apps.get_models() if history_manager(model) is not None
        }
        encontrados = {model for models in dashboard_data.tracked_apps().values() for model in models}
        assert encontrados == esperados
        assert len(encontrados) > 50
        assert "core" not in dashboard_data.tracked_apps()  # ningún modelo de core tiene historial

    def test_las_etiquetas_no_se_repiten_dentro_de_una_app(self):
        # el gráfico arma una serie por etiqueta: dos modelos con el mismo plural se pisarían
        for app_label, models in dashboard_data.tracked_apps().items():
            etiquetas = [dashboard_data.model_label(model) for model in models]
            with self.subTest(app=app_label):
                assert len(etiquetas) == len(set(etiquetas))

    @override_settings(DASHBOARD_EXCLUDED_MODELS=["personalizador.TipoLicenciaPermiso"])
    def test_modelos_excluidos(self):
        assert TipoLicenciaPermiso not in dashboard_data.tracked_apps()["personalizador"]
        TipoLicenciaPermiso.objects.create(tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre="Excluido")
        cambios, _ = dashboard_data.changes_feed("personalizador")
        assert "Tipos de Licencias/Permisos" not in {c["modelo"] for c in cambios}


@aislar_dashboard
class ChangesFeedTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")

    def tipos(self, cantidad):
        for numero in range(cantidad):
            TipoLicenciaPermiso.objects.create(tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre=f"Tipo {numero}")

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

        cambios, hay_mas = dashboard_data.changes_feed("personalizador", "tipolicenciapermiso")
        assert hay_mas is False
        assert [c["tipo"] for c in cambios] == ["Eliminado", "Modificado", "Creado"]
        assert {c["modelo"] for c in cambios} == {"Tipos de Licencias/Permisos"}
        assert {c["usuario"] for c in cambios} == {self.user}
        assert cambios[-1]["objeto"] == "Art. 1 - Razones particulares (Permiso)"
        assert cambios[0]["objeto"] == "Art. 1 - Renombrado (Permiso)"

    def test_mezcla_los_modelos_de_la_app_por_fecha(self):
        crear_tipo = lambda nombre: TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre=nombre,
        )
        crear_tipo("Primero")
        GeneroAgente.objects.create(generoagente_nombre="Género nuevo")
        crear_tipo("Último")
        cambios, _ = dashboard_data.changes_feed("personalizador", limit=3)
        assert [c["modelo"] for c in cambios] == ["Tipos de Licencias/Permisos", "Géneros", "Tipos de Licencias/Permisos"]
        fechas = [c["fecha"] for c in cambios]
        assert fechas == sorted(fechas, reverse=True)

    def test_paginas(self):
        self.tipos(5)
        objetos = lambda **kwargs: [c["objeto"] for c in dashboard_data.changes_feed("personalizador", "tipolicenciapermiso", **kwargs)[0]]
        assert objetos(limit=3) == ["None - Tipo 4 (Permiso)", "None - Tipo 3 (Permiso)", "None - Tipo 2 (Permiso)"]
        assert objetos(limit=3, offset=3) == ["None - Tipo 1 (Permiso)", "None - Tipo 0 (Permiso)"]
        assert objetos(limit=3, offset=6) == []
        hay_mas = lambda **kwargs: dashboard_data.changes_feed("personalizador", "tipolicenciapermiso", **kwargs)[1]
        assert hay_mas(limit=3) is True
        assert hay_mas(limit=5) is False  # justo entran: no hay otra página
        assert hay_mas(limit=3, offset=3) is False

    def test_un_modelo_que_no_es_de_la_app_no_trae_nada(self):
        self.tipos(1)
        assert dashboard_data.changes_feed("personalizador", "obra") == ([], False)

    def test_un_str_que_falla_cae_al_texto_de_respaldo(self):
        self.tipos(2)
        with mock.patch.object(TipoLicenciaPermiso, "__str__", side_effect=AttributeError("roto")):
            cambios, _ = dashboard_data.changes_feed("personalizador", "tipolicenciapermiso")
        pks = sorted(TipoLicenciaPermiso.objects.values_list("pk", flat=True), reverse=True)
        assert [c["objeto"] for c in cambios] == [f"Tipo de Licencia/Permiso #{pk}" for pk in pks]


@aislar_dashboard
class ChangesFeedRelacionadosTest(TestCase):
    """Con modelos de carga cuyo __str__ recorre relacionados (etapa -> rubro -> plan ->
    obra -> empresa) y con el único modelo de main que tiene una geometría (Obra)."""

    def setUp(self):
        empresa = Empresa.objects.create(empresa_nombre="Empresa Test")
        programa = Programa.objects.create(programa_nombre="Programa Test")
        self.obra = Obra.objects.create(
            obra_nombre="Obra Test", obra_empresa=empresa, obra_programa=programa, obra_expediente="EXP-D1"
        )
        plan = PlanDeTrabajos.objects.create(trabajos_obra=self.obra, trabajos_fecha=date(2026, 1, 1))
        rubro_certificado = CertificadoRubro.objects.create(certificadorubro_nombre="Vivienda", certificadorubro_nombre_corto="V")
        self.rubro = PlanDeTrabajosRubro.objects.create(
            rubro_plan=plan, rubro_nombre="Vivienda", rubro_presupuesto=Decimal("1000"),
            rubro_certificado_rubro=rubro_certificado,
        )

    def consultas_del_feed(self, modelo):
        with CaptureQueriesContext(connection) as consultas:
            cambios, _ = dashboard_data.changes_feed("carga", modelo)
        return cambios, consultas

    def test_la_cantidad_de_consultas_no_depende_de_la_cantidad_de_filas(self):
        for _ in range(3):
            PlanDeTrabajosEtapa.objects.create(etapa_rubro=self.rubro)
        cambios, con_tres = self.consultas_del_feed("plandetrabajosetapa")
        assert len(cambios) == 3
        for _ in range(9):
            PlanDeTrabajosEtapa.objects.create(etapa_rubro=self.rubro)
        cambios, con_doce = self.consultas_del_feed("plandetrabajosetapa")
        assert len(cambios) == 12
        assert len(con_doce) == len(con_tres)
        # y el texto es el mismo que daría el __str__ del objeto real
        assert {c["objeto"] for c in cambios} == {str(etapa) for etapa in PlanDeTrabajosEtapa.objects.all()}

    def test_un_padre_borrado_cae_al_texto_de_respaldo_sin_romper_a_los_demas(self):
        etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=self.rubro)
        huerfana = PlanDeTrabajosEtapa.objects.create(etapa_rubro=self.rubro)
        # la fila histórica sobrevive apuntando a un rubro que ya no está
        history_manager(PlanDeTrabajosEtapa).filter(id=huerfana.pk).update(etapa_rubro_id=999999)
        cambios, _ = self.consultas_del_feed("plandetrabajosetapa")
        assert {c["objeto"] for c in cambios} == {str(etapa), f"Etapa Proyectada de Plan de Trabajos #{huerfana.pk}"}

    def test_no_trae_las_geometrias(self):
        assert dashboard_data._heavy_fields(history_manager(Obra).model) == ["obra_georeferencia"]
        cambios, consultas = self.consultas_del_feed("obra")
        assert [c["objeto"] for c in cambios] == [str(self.obra)]
        assert not any("obra_georeferencia" in consulta["sql"] for consulta in consultas)


@aislar_dashboard
class DashboardChangesViewTest(TestCase):
    URL = "/administracion/dashboard/cambios/personalizador/"

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def entrar(self):
        self.client.login(username="admin_user", password="pass1234!")

    def tipos(self, cantidad):
        for numero in range(cantidad):
            TipoLicenciaPermiso.objects.create(tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre=f"Tipo {numero:02}")

    def test_solo_superusuarios(self):
        assert self.client.get(self.URL).status_code == 302
        self.client.login(username="plain_user", password="pass1234!")
        assert self.client.get(self.URL).status_code == 403

    def test_app_o_modelo_desconocidos(self):
        self.entrar()
        assert self.client.get("/administracion/dashboard/cambios/no-existe/").status_code == 404
        assert self.client.get("/administracion/dashboard/cambios/core/").status_code == 404  # sin historial
        assert self.client.get(self.URL, {"modelo": "obra"}).status_code == 404  # es de otra app

    def test_es_un_fragmento_con_el_filtro_de_modelos(self):
        self.entrar()
        self.tipos(1)
        resp = self.client.get(self.URL)
        assert resp.status_code == 200
        self.assertNotContains(resp, "<html")
        self.assertContains(resp, "None - Tipo 00 (Permiso)")
        self.assertContains(resp, '<option value="tipolicenciapermiso">Tipos de Licencias/Permisos</option>', html=True)
        assert len(resp.context["models"]) == len(dashboard_data.tracked_apps()["personalizador"])

    def test_filtra_por_modelo(self):
        self.entrar()
        self.tipos(1)
        GeneroAgente.objects.create(generoagente_nombre="Género nuevo")
        resp = self.client.get(self.URL, {"modelo": "generoagente"})
        self.assertContains(resp, "Género nuevo")
        self.assertNotContains(resp, "Tipo 00")
        self.assertContains(resp, '<option value="generoagente" selected>Géneros</option>', html=True)

    def test_paginas(self):
        self.entrar()
        self.tipos(dashboard_data.CHANGES_PAGE_SIZE + 2)
        filtro = {"modelo": "tipolicenciapermiso"}
        primera = self.client.get(self.URL, filtro)
        assert len(primera.context["changes"]) == dashboard_data.CHANGES_PAGE_SIZE
        assert primera.context["next_page"] == 2
        self.assertContains(primera, "Tipo 51")
        self.assertNotContains(primera, "Tipo 01 ")
        # el botón de la página siguiente conserva el filtro
        self.assertContains(primera, f'hx-get="{self.URL}?modelo=tipolicenciapermiso&amp;pagina=2"')

        segunda = self.client.get(self.URL, {**filtro, "pagina": 2})
        assert [c["objeto"] for c in segunda.context["changes"]] == ["None - Tipo 01 (Permiso)", "None - Tipo 00 (Permiso)"]
        assert segunda.context["next_page"] is None
        self.assertContains(segunda, f'hx-get="{self.URL}?modelo=tipolicenciapermiso&amp;pagina=1"')

    def test_una_pagina_invalida_es_la_primera(self):
        self.entrar()
        for valor in ("abc", "0", "-3"):
            with self.subTest(valor=valor):
                assert self.client.get(self.URL, {"pagina": valor}).context["page"] == 1

    def test_si_falla_muestra_no_disponible(self):
        self.entrar()
        with (
            mock.patch("core.dashboard_data.changes_feed", side_effect=RuntimeError("roto")),
            self.assertLogs("core.views", "ERROR"),
        ):
            resp = self.client.get(self.URL)
        assert resp.status_code == 200
        self.assertContains(resp, "No disponible")


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


class RegistrarLoginTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")

    def entrar(self, **meta):
        # Client.login() arma un request pelado, sin cabeceras: se dispara la señal con
        # uno que las tenga, como hace django.contrib.auth.login().
        request = RequestFactory().post("/accounts/login/", **meta)
        user_logged_in.send(sender=UserModel, request=request, user=self.user)

    def test_guarda_la_ip_de_x_forwarded_for(self):
        self.entrar(HTTP_X_FORWARDED_FOR="10.106.16.50, 127.0.0.1")
        assert LoginEvent.objects.get().ip_address == "10.106.16.50"

    def test_sin_x_forwarded_for_usa_remote_addr(self):
        self.entrar(REMOTE_ADDR="192.168.0.7")
        assert LoginEvent.objects.get().ip_address == "192.168.0.7"

    def test_un_x_forwarded_for_que_no_es_una_ip_no_rompe_el_login(self):
        for valor in ("no-es-una-ip", "10.0.0.1:4321", "' OR 1=1", ""):
            with self.subTest(valor=valor):
                LoginEvent.objects.all().delete()
                self.entrar(HTTP_X_FORWARDED_FOR=valor, REMOTE_ADDR="192.168.0.7")
                assert LoginEvent.objects.get().ip_address == "192.168.0.7"

    def test_sin_ninguna_ip_valida_queda_vacia(self):
        self.entrar(HTTP_X_FORWARDED_FOR="desconocido", REMOTE_ADDR="")
        assert LoginEvent.objects.get().ip_address is None

    def test_si_no_se_puede_registrar_el_login_sigue(self):
        cliente = Client()
        with (
            mock.patch("core.signals.LoginEvent.objects.create", side_effect=DatabaseError("roto")),
            self.assertLogs("core.signals", "ERROR"),
        ):
            assert cliente.login(username="plain_user", password="pass1234!")
        assert not LoginEvent.objects.exists()
        # la sesión quedó abierta
        assert cliente.get("/administracion/dashboard/").status_code == 403

    def test_un_insert_fallido_no_deja_abortada_la_transaccion(self):
        def insert_roto(**kwargs):
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tabla_que_no_existe")

        with mock.patch("core.signals.LoginEvent.objects.create", insert_roto), self.assertLogs("core.signals", "ERROR"):
            self.entrar()
        assert UserModel.objects.filter(pk=self.user.pk).exists()
