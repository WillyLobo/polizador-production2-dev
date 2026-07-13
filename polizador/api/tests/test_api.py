import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.middleware.csrf import get_token
from django.test import RequestFactory, TestCase, Client
from ninja.testing import TestClient
from api.router import api

UserModel = get_user_model()


class HealthCheckTest(TestCase):
    def setUp(self):
        self.client = TestClient(api)

    def test_health_check(self):
        resp = self.client.get("__version__")
        assert resp.status_code == 200
        data = resp.json()
        assert "version" in data and data["version"] == "1.0.0"


class AuthTest(TestCase):
    """Test that unauthenticated requests to protected endpoints return 401."""

    def setUp(self):
        self.client = TestClient(api)

    def test_receptors_requires_auth(self):
        resp = self.client.get("receptores/")
        assert resp.status_code == 401

    def test_aseguradoras_requires_auth(self):
        resp = self.client.get("aseguradoras/")
        assert resp.status_code == 401

    def test_users_requires_auth(self):
        resp = self.client.get("users/")
        assert resp.status_code == 401


class LoadDataMixin:
    """Shared mixin to pre-load reference data for tests."""

    def setUp(self):
        super().setUp()
        from carga.models import (
            Aseguradora, Empresa, Obra, Programa, Region,
            CertificadoRubro, CertificadoFinanciamiento,
        )
        from personalizador.models import CargoTipo, Directorio, Gerencia, Direccion

        self.aseguradora = Aseguradora.objects.create(aseguradora_nombre="Aseguradora Test")
        self.programa = Programa.objects.create(programa_nombre="Programa Test")
        self.region = Region.objects.create(region_numero="1")
        self.empresas = Empresa.objects.create(empresa_nombre="Empresa Test", empresa_cuit="12345678901")
        self.rubro = CertificadoRubro.objects.create(certificadorubro_nombre="Vivienda", certificadorubro_nombre_corto="V")
        self.finan = CertificadoFinanciamiento.objects.create(
            certificadofinanciamiento_nombre="Nación",
            certificadofinanciamiento_nombre_corto="N"
        )

        CargoTipo.objects.get_or_create(cargotipo="Arquitecto")
        directorio, _ = Directorio.objects.get_or_create(directorio_nombre="Presidencia", directorio_cuof="D001")
        Gerencia.objects.get_or_create(
            gerencia_nombre="Gerencia Test", gerencia_cuof="G001", gerencia_directorio=directorio,
        )


class ObraAPITest(LoadDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient(api)

    def test_list_obras_empty(self):
        resp = self.client.get("obras/")
        assert resp.status_code == 401

    def test_create_obra_fails_unauth(self):
        resp = self.client.post(
            "obras/",
            json={
                "obra_nombre": "Nueva Obra Test",
                "empresa_id": self.empresas.id,
                "programa_id": self.programa.id,
                "expediente": "EXP-2026-001",
            },
        )
        # Auth failure or validation error expected (not 201)
        assert resp.status_code != 201


class ModeloAPITest(LoadDataMixin, TestCase):
    """Test CRUD for several models."""

    def setUp(self):
        super().setUp()
        self.client = TestClient(api)

    def test_list_aseguradoras_empty(self):
        resp = self.client.get("aseguradoras/")
        assert resp.status_code == 401


class SchemaTest(TestCase):
    """Test that schemas import correctly."""

    def test_carga_schemas_import(self):
        from api.schemas.carga_schemas import (
            AseguradoraOut, EmpresaOut, ObraOut, CertificadoOut,
        )
        assert AseguradoraOut.model_fields is not None
        assert len(AseguradoraOut.model_fields) > 0

    def test_secretariador_schemas_import(self):
        from api.schemas.secretariador_schemas import (
            SolicitudOut, ComisionadoOut,
        )
        assert SolicitudOut.model_fields is not None

    def test_personalizador_schemas_import(self):
        from api.schemas.personalizador_schemas import (
            GerenciaOut, DireccionOut, DepartamentoPerOut, CustomUserOut,
        )
        assert GerenciaOut.model_fields is not None
        assert CustomUserOut.model_fields is not None


class OpenAPITest(TestCase):
    """Test that OpenAPI schema is accessible via Django URLconf."""

    def setUp(self):
        self.client = Client()

    def test_openapi_schema_available(self):
        # /v1/api/openapi.json is staff-only too (same docs_decorator as /docs).
        staff = UserModel.objects.create_user(username="openapi_staff", password="pass1234!", is_staff=True)
        self.client.login(username="openapi_staff", password="pass1234!")
        resp = self.client.get("/v1/api/openapi.json")
        assert resp.status_code == 200
        data = resp.json()
        assert "paths" in data or "info" in data

    def test_docs_url_available(self):
        # /v1/api/docs is staff-only (docs_decorator=staff_member_required in api/router.py).
        staff = UserModel.objects.create_user(username="docs_staff", password="pass1234!", is_staff=True)
        self.client.login(username="docs_staff", password="pass1234!")
        resp = self.client.get("/v1/api/docs")
        # Should return HTML (status 200) for Swagger UI
        assert resp.status_code == 200


class ModelPermissionEnforcementTest(TestCase):
    """A logged-in user with no Django permissions must be rejected (403);
    granting the matching `carga.<action>_receptor` permission must let it through."""

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.client.login(username="plain_user", password="pass1234!")

    def test_create_receptor_forbidden_without_permission(self):
        resp = self.client.post(
            "/v1/api/receptores/",
            data=json.dumps({"receptor_nombre": "Test"}),
            content_type="application/json",
        )
        assert resp.status_code == 403

    def test_create_receptor_allowed_with_permission(self):
        perm = Permission.objects.get(codename="add_receptor", content_type__app_label="carga")
        self.user.user_permissions.add(perm)
        resp = self.client.post(
            "/v1/api/receptores/",
            data=json.dumps({"receptor_nombre": "Test"}),
            content_type="application/json",
        )
        assert resp.status_code in (200, 201)

    def test_list_receptores_forbidden_without_view_permission(self):
        resp = self.client.get("/v1/api/receptores/")
        assert resp.status_code == 403

    def test_delete_receptor_forbidden_without_permission(self):
        from carga.models import Receptor

        r = Receptor.objects.create(receptor_nombre="Test")
        resp = self.client.delete(f"/v1/api/receptor/{r.id}/")
        assert resp.status_code == 403


class CsrfEnforcementTest(TestCase):
    """POST/PUT/DELETE must be rejected without a valid CSRF token, even for an
    authenticated + permissioned user, since the API relies on session cookies."""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = UserModel.objects.create_user(username="csrf_user", password="pass1234!")
        perm = Permission.objects.get(codename="add_receptor", content_type__app_label="carga")
        self.user.user_permissions.add(perm)
        self.client.login(username="csrf_user", password="pass1234!")

    def test_post_without_csrf_token_rejected(self):
        resp = self.client.post(
            "/v1/api/receptores/",
            data=json.dumps({"receptor_nombre": "Test"}),
            content_type="application/json",
        )
        assert resp.status_code == 403

    def test_post_with_valid_csrf_token_accepted(self):
        token = get_token(RequestFactory().get("/"))
        self.client.cookies["csrftoken"] = token
        resp = self.client.post(
            "/v1/api/receptores/",
            data=json.dumps({"receptor_nombre": "Test"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        assert resp.status_code in (200, 201)


class ObraDatatableAPITest(LoadDataMixin, TestCase):
    """/v1/api/datatables/obras/ and its row-detail endpoint (ninja replacement for
    ListaObrasView / django-ajax-datatable)."""

    def setUp(self):
        super().setUp()
        from carga.models import Obra

        self.obra_a = Obra.objects.create(
            obra_nombre="Escuela Norte", obra_empresa=self.empresas,
            obra_programa=self.programa, obra_expediente="EXP-A",
        )
        self.obra_b = Obra.objects.create(
            obra_nombre="Hospital Sur", obra_empresa=self.empresas,
            obra_programa=self.programa, obra_expediente="EXP-B",
        )
        self.anon_client = TestClient(api)
        self.client = Client()
        self.user = UserModel.objects.create_user(username="obras_user", password="pass1234!")
        self.client.login(username="obras_user", password="pass1234!")

    def test_requires_auth(self):
        resp = self.anon_client.get("datatables/obras/")
        assert resp.status_code == 401

    def test_forbidden_without_view_permission(self):
        resp = self.client.get("/v1/api/datatables/obras/")
        assert resp.status_code == 403

    def _grant_view_perm(self):
        perm = Permission.objects.get(codename="view_obra", content_type__app_label="carga")
        self.user.user_permissions.add(perm)

    def test_lists_rows_with_permission(self):
        self._grant_view_perm()
        resp = self.client.get("/v1/api/datatables/obras/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["recordsTotal"] == 2
        assert data["recordsFiltered"] == 2
        names = {row["obra_nombre"] for row in data["data"]}
        assert names == {"Escuela Norte", "Hospital Sur"}
        assert "acciones" in data["data"][0]

    def test_search_filters_rows(self):
        self._grant_view_perm()
        resp = self.client.get("/v1/api/datatables/obras/", {"search": "Escuela"})
        data = resp.json()
        assert data["recordsTotal"] == 2
        assert data["recordsFiltered"] == 1
        assert data["data"][0]["obra_nombre"] == "Escuela Norte"

    def test_order_by_obra_nombre(self):
        self._grant_view_perm()
        resp = self.client.get("/v1/api/datatables/obras/", {"order_by": "obra_nombre"})
        data = resp.json()
        assert [row["obra_nombre"] for row in data["data"]] == ["Escuela Norte", "Hospital Sur"]

    def test_column_filter_narrows_rows(self):
        self._grant_view_perm()
        resp = self.client.get(
            "/v1/api/datatables/obras/",
            {"filters": json.dumps({"obra_nombre": "Hospital"})},
        )
        data = resp.json()
        assert data["recordsTotal"] == 2
        assert data["recordsFiltered"] == 1
        assert data["data"][0]["obra_nombre"] == "Hospital Sur"

    def test_detalle_requires_permission(self):
        resp = self.client.get(f"/v1/api/datatables/obras/{self.obra_a.id}/detalle/")
        assert resp.status_code == 403

    def test_detalle_renders_html(self):
        self._grant_view_perm()
        resp = self.client.get(f"/v1/api/datatables/obras/{self.obra_a.id}/detalle/")
        assert resp.status_code == 200
        assert "html" in resp.json()


class SolicitudDatatableAPITest(TestCase):
    """/v1/api/datatables/solicitudes/ and its row-detail/filtro-vehiculos endpoints
    (ninja replacement for ListaSolicitudesView / django-ajax-datatable)."""

    def setUp(self):
        from carga.models import Provincia
        from personalizador.models import Agente, GeneroAgente
        from secretariador.models import (
            ComisionadoSolicitud, InstrumentosLegalesDecretos, MontoViaticoDiario, Solicitud, Vehiculo,
        )

        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.agente = Agente.objects.create(
            agente_nombres="Juan", agente_apellidos="Perez",
            sexo=genero, dni=30111222, cuil="20301112223",
        )
        self.provincia = Provincia.objects.create(id=1, provincia_nombre="Chaco")
        decreto = InstrumentosLegalesDecretos.objects.create(
            instrumentolegaldecretos_numero="100", instrumentolegaldecretos_ano="2026",
        )
        self.monto_viatico = MontoViaticoDiario.objects.create(montoviaticodiario_decreto_reglamentario=decreto)
        self.vehiculo = Vehiculo.objects.create(vehiculo_modelo="Ford Ranger", vehiculo_patente="AA123BB")

        self.solicitud_a = Solicitud.objects.create(
            solicitud_actuacion_ano=2026, solicitud_actuacion_numero=1,
            solicitud_solicitante=self.agente, solicitud_provincia=self.provincia,
            solicitud_decreto_viaticos=self.monto_viatico,
            solicitud_fecha_desde="2026-01-10", solicitud_fecha_hasta="2026-01-12",
            solicitud_tareas="Inspección de obra en Resistencia " + "x" * 100,
            solicitud_vehiculo=self.vehiculo, solicitud_dia_inhabil=False,
        )
        self.solicitud_b = Solicitud.objects.create(
            solicitud_actuacion_ano=2026, solicitud_actuacion_numero=2,
            solicitud_solicitante=self.agente, solicitud_provincia=self.provincia,
            solicitud_decreto_viaticos=self.monto_viatico,
            solicitud_fecha_desde="2026-02-10", solicitud_fecha_hasta="2026-02-12",
            solicitud_tareas="Reunión breve", solicitud_dia_inhabil=True,
            solicitud_anulada=True,
        )
        self.agente_comisionado = Agente.objects.create(
            agente_nombres="Maria", agente_apellidos="Gomez",
            sexo=genero, dni=30222333, cuil="27302223334",
        )
        ComisionadoSolicitud.objects.create(
            comisionadosolicitud_foreign=self.solicitud_a,
            comisionadosolicitud_nombre=self.agente_comisionado,
            comisionadosolicitud_colaborador=False,
            comisionadosolicitud_chofer=False,
        )

        self.anon_client = TestClient(api)
        self.client = Client()
        self.user = UserModel.objects.create_user(username="solicitudes_user", password="pass1234!")
        self.client.login(username="solicitudes_user", password="pass1234!")

    def _grant_view_perm(self):
        perm = Permission.objects.get(codename="view_solicitud", content_type__app_label="secretariador")
        self.user.user_permissions.add(perm)

    def test_requires_auth(self):
        resp = self.anon_client.get("datatables/solicitudes/")
        assert resp.status_code == 401

    def test_forbidden_without_permission(self):
        resp = self.client.get("/v1/api/datatables/solicitudes/")
        assert resp.status_code == 403

    def test_lists_rows_and_truncates_tareas(self):
        self._grant_view_perm()
        resp = self.client.get("/v1/api/datatables/solicitudes/")
        data = resp.json()
        assert data["recordsTotal"] == 2

        row_a = next(r for r in data["data"] if r["id"] == self.solicitud_a.id)
        assert "&hellip;" in row_a["solicitud_tareas"]
        assert row_a["solicitud_tareas"].startswith('<span title=')
        assert row_a["solicitud_vehiculo"] == "Ford Ranger - AA123BB"
        assert row_a["solicitud_dia_inhabil"] == "No"

        row_b = next(r for r in data["data"] if r["id"] == self.solicitud_b.id)
        assert row_b["solicitud_dia_inhabil"] == "Sí"
        assert row_b["solicitud_anulada"] is True

    def test_default_order_is_by_actuacion_desc(self):
        self._grant_view_perm()
        resp = self.client.get("/v1/api/datatables/solicitudes/")
        data = resp.json()
        assert [r["id"] for r in data["data"]] == [self.solicitud_b.id, self.solicitud_a.id]

    def test_filter_by_vehiculo(self):
        self._grant_view_perm()
        resp = self.client.get(
            "/v1/api/datatables/solicitudes/",
            {"filters": json.dumps({"solicitud_vehiculo": str(self.vehiculo.id)})},
        )
        data = resp.json()
        assert data["recordsFiltered"] == 1
        assert data["data"][0]["id"] == self.solicitud_a.id

    def test_filter_by_fecha_desde(self):
        self._grant_view_perm()
        resp = self.client.get(
            "/v1/api/datatables/solicitudes/",
            {"filters": json.dumps({"solicitud_fecha_desde": "2026-02-10"})},
        )
        data = resp.json()
        assert data["recordsFiltered"] == 1
        assert data["data"][0]["id"] == self.solicitud_b.id

    def test_filter_by_comisionados(self):
        self._grant_view_perm()
        resp = self.client.get(
            "/v1/api/datatables/solicitudes/",
            {"filters": json.dumps({"Comisionados": "Gomez"})},
        )
        data = resp.json()
        assert data["recordsFiltered"] == 1
        assert data["data"][0]["id"] == self.solicitud_a.id
        assert "Maria Gomez" in data["data"][0]["Comisionados"]

    def test_filtro_vehiculos_choices(self):
        self._grant_view_perm()
        resp = self.client.get("/v1/api/datatables/solicitudes/filtro-vehiculos/")
        assert resp.status_code == 200
        assert [self.vehiculo.id, "Ford Ranger - AA123BB"] in resp.json()["choices"]

    def test_detalle_renders_html(self):
        self._grant_view_perm()
        resp = self.client.get(f"/v1/api/datatables/solicitudes/{self.solicitud_a.id}/detalle/")
        assert resp.status_code == 200


# --- Remaining ~19 datatable listings migrated from AjaxDatatableView-based CBVs ---

NEW_DATATABLE_LIST_URLS = [
    "datatables/aseguradoras/",
    "datatables/empresas/",
    "datatables/programas/",
    "datatables/regiones/",
    "datatables/departamentos-carga/",
    "datatables/municipios/",
    "datatables/localidades/",
    "datatables/conjuntos/",
    "datatables/representantes-tecnicos/",
    "datatables/comisionados/",
    "datatables/vehiculos/",
    "datatables/obras-extendida/",
    "datatables/polizas/",
    "datatables/certificados/",
    "datatables/incorporaciones/",
    "datatables/memorandums/",
    "datatables/decretos/",
    "datatables/resoluciones/",
    "datatables/resoluciones-directorio/",
]


class NewDatatableAuthTest(TestCase):
    """Every migrated datatable listing must reject anonymous requests."""

    def setUp(self):
        self.client = TestClient(api)

    def test_all_new_datatables_require_auth(self):
        for url in NEW_DATATABLE_LIST_URLS:
            resp = self.client.get(url)
            assert resp.status_code == 401, f"{url} did not return 401 for anonymous request"


class SimpleLookupDatatableTest(LoadDataMixin, TestCase):
    """Aseguradora/Empresa/Programa/Region/Departamento/Municipio/Localidad/Conjunto
    listings, all built with api.views.generics.register_simple_datatable."""

    def setUp(self):
        super().setUp()
        from carga.models import ConjuntoLicitado, Departamento, Localidad, Municipio

        self.departamento = Departamento.objects.create(id=1, departamento_nombre="Departamento Test")
        self.municipio = Municipio.objects.create(
            id=1, municipio_nombre="Municipio Test", municipio_departamento=self.departamento, municipio_region=self.region,
        )
        self.localidad = Localidad.objects.create(
            id=1, localidad_nombre="Localidad Test", localidad_funcion="Cabecera",
            localidad_departamento=self.departamento, localidad_municipio=self.municipio,
        )
        self.conjunto = ConjuntoLicitado.objects.create(conjunto_nombre="Conjunto Test")

        self.user = UserModel.objects.create_user(username="lookup_user", password="pass1234!")
        self.client = Client()
        self.client.login(username="lookup_user", password="pass1234!")

    def _grant(self, codename, app_label="carga"):
        perm = Permission.objects.get(codename=codename, content_type__app_label=app_label)
        self.user.user_permissions.add(perm)

    def test_forbidden_without_permission(self):
        resp = self.client.get("/v1/api/datatables/aseguradoras/")
        assert resp.status_code == 403

    def test_aseguradoras_lists_rows(self):
        self._grant("view_aseguradora")
        resp = self.client.get("/v1/api/datatables/aseguradoras/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert data["data"][0]["aseguradora_nombre"] == "Aseguradora Test"
        assert "acciones" in data["data"][0]

    def test_empresas_lists_rows(self):
        self._grant("view_empresa")
        resp = self.client.get("/v1/api/datatables/empresas/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert data["data"][0]["empresa_nombre"] == "Empresa Test"

    def test_programas_lists_rows(self):
        self._grant("view_programa")
        resp = self.client.get("/v1/api/datatables/programas/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert data["data"][0]["programa_nombre"] == "Programa Test"

    def test_regiones_lists_rows(self):
        self._grant("view_region")
        resp = self.client.get("/v1/api/datatables/regiones/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert data["data"][0]["region_numero"] == "1"

    def test_departamentos_lists_rows(self):
        self._grant("view_departamento")
        resp = self.client.get("/v1/api/datatables/departamentos-carga/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert data["data"][0]["departamento_nombre"] == "Departamento Test"

    def test_municipios_lists_rows_with_foreign_fields(self):
        self._grant("view_municipio")
        resp = self.client.get("/v1/api/datatables/municipios/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        row = data["data"][0]
        assert row["municipio_nombre"] == "Municipio Test"
        assert row["municipio_departamento"] == "Departamento Test"
        assert row["municipio_region"] == "1"

    def test_localidades_filter_funcion(self):
        self._grant("view_localidad")
        resp = self.client.get("/v1/api/datatables/localidades/filtro-funcion/")
        assert resp.status_code == 200
        assert ["Cabecera", "Cabecera"] in resp.json()["choices"]

        resp = self.client.get(
            "/v1/api/datatables/localidades/", {"filters": json.dumps({"localidad_funcion": "Cabecera"})},
        )
        data = resp.json()
        assert data["recordsFiltered"] == 1
        assert data["data"][0]["localidad_nombre"] == "Localidad Test"

    def test_conjuntos_lists_rows(self):
        self._grant("view_conjuntolicitado")
        resp = self.client.get("/v1/api/datatables/conjuntos/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert data["data"][0]["conjunto_nombre"] == "Conjunto Test"


class PersonalizadorSimpleDatatableTest(TestCase):
    """RepresentanteTecnico, Agente (Comisionados) and Vehiculo listings."""

    def setUp(self):
        from personalizador.models import (
            Agente, CargoTipo, GeneroAgente, Oficina, RepresentanteTecnico, TituloProfesional,
        )
        from secretariador.models import Vehiculo

        self.titulo = TituloProfesional.objects.create(
            tituloprofesional_nombre="Arquitecto", tituloprofesional_grado="Universitario",
        )
        self.representante = RepresentanteTecnico.objects.create(
            representantetecnico_nombre="Juan", representantetecnico_apellido="Perez",
            representantetecnico_dni=25111222, representantetecnico_cuil="20251112223",
            representantetecnico_profesion=self.titulo, representantetecnico_matricula="M-100",
        )

        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        cargo_tipo = CargoTipo.objects.create(cargotipo="Arquitecto Comisionado")
        oficina = Oficina.objects.create(cargo_tipo=cargo_tipo)
        self.agente = Agente.objects.create(
            agente_nombres="Maria", agente_apellidos="Gomez", sexo=genero, dni=30333444,
            cuil="27303334445", oficina=oficina, agente_personal_transitorio=True,
        )

        self.vehiculo = Vehiculo.objects.create(
            vehiculo_caracter="O", vehiculo_modelo="Toyota Hilux", vehiculo_patente="AB123CD",
        )

        self.user = UserModel.objects.create_user(username="pers_user", password="pass1234!")
        self.client = Client()
        self.client.login(username="pers_user", password="pass1234!")

    def _grant(self, codename, app_label):
        perm = Permission.objects.get(codename=codename, content_type__app_label=app_label)
        self.user.user_permissions.add(perm)

    def test_representantes_tecnicos_lists_rows(self):
        self._grant("view_representantetecnico", "personalizador")
        resp = self.client.get("/v1/api/datatables/representantes-tecnicos/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        row = data["data"][0]
        assert row["representantetecnico_nombre"] == "Juan"
        assert row["representantetecnico_profesion"] == "Arquitecto"

    def test_comisionados_lists_rows_and_filters_boolean(self):
        self._grant("view_agente", "personalizador")
        resp = self.client.get("/v1/api/datatables/comisionados/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        row = data["data"][0]
        assert row["agente_apellidos"] == "Gomez"
        assert row["oficina"] == "Arquitecto Comisionado"
        assert row["agente_personal_transitorio"] == "Sí"

        resp = self.client.get(
            "/v1/api/datatables/comisionados/",
            {"filters": json.dumps({"agente_personal_de_gabinete": "true"})},
        )
        assert resp.json()["recordsFiltered"] == 0

    def test_vehiculos_lists_rows_with_display_choice(self):
        self._grant("view_vehiculo", "secretariador")
        resp = self.client.get("/v1/api/datatables/vehiculos/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert data["data"][0]["vehiculo_caracter"] == "Oficial"


class ObraExtendidaDatatableTest(LoadDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        from carga.models import Obra

        self.obra = Obra.objects.create(
            obra_nombre="Escuela Test", obra_empresa=self.empresas, obra_programa=self.programa,
            obra_expediente="EXP-EXT-1", obra_licitacion_tipo="L",
        )
        self.user = UserModel.objects.create_user(username="obraext_user", password="pass1234!")
        self.client = Client()
        self.client.login(username="obraext_user", password="pass1234!")
        perm = Permission.objects.get(codename="view_obra", content_type__app_label="carga")
        self.user.user_permissions.add(perm)

    def test_lists_rows_with_formatted_columns(self):
        resp = self.client.get("/v1/api/datatables/obras-extendida/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["recordsTotal"] == 1
        row = data["data"][0]
        assert row["obra_nombre"].startswith('<span title=')
        assert row["obra_empresa"] == "Empresa Test"
        assert row["obra_licitacion_tipo"] == "Licitación Pública"
        assert row["obra_contrato_nacion_pesos"] == "0,00"

    def test_filtro_programa_and_ano_choices(self):
        resp = self.client.get("/v1/api/datatables/obras-extendida/filtro-programa/")
        assert [self.programa.id, "Programa Test"] in resp.json()["choices"]

    def test_filter_by_programa(self):
        resp = self.client.get(
            "/v1/api/datatables/obras-extendida/",
            {"filters": json.dumps({"obra_programa": str(self.programa.id)})},
        )
        assert resp.json()["recordsFiltered"] == 1


class PolizaCertificadoDatatableTest(LoadDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        from carga.models import Certificado, Obra, Poliza

        self.obra = Obra.objects.create(
            obra_nombre="Obra Poliza Test", obra_empresa=self.empresas, obra_programa=self.programa,
            obra_expediente="EXP-POL-1",
        )
        self.poliza = Poliza.objects.create(
            poliza_fecha="2026-01-10", poliza_expediente="EXP-POL-1", poliza_numero=1001,
            poliza_concepto="C", poliza_recibo="REC-1", poliza_aseguradora=self.aseguradora,
            poliza_tomador=self.empresas, poliza_obra=self.obra,
        )
        self.certificado = Certificado.objects.create(
            certificado_obra=self.obra, certificado_expediente="EXP-CERT-1", certificado_rubro_db=self.rubro,
        )

        self.user = UserModel.objects.create_user(username="poliza_user", password="pass1234!")
        self.client = Client()
        self.client.login(username="poliza_user", password="pass1234!")

    def _grant(self, codename):
        perm = Permission.objects.get(codename=codename, content_type__app_label="carga")
        self.user.user_permissions.add(perm)

    def test_polizas_lists_rows(self):
        self._grant("view_poliza")
        resp = self.client.get("/v1/api/datatables/polizas/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        row = data["data"][0]
        assert row["poliza_concepto"] == "Garantía de Ejecución de Contrato"
        assert row["poliza_aseguradora"] == "Aseguradora Test"
        assert row["poliza_editor"] == ""

    def test_certificados_lists_rows_and_filtro_rubro(self):
        self._grant("view_certificado")
        resp = self.client.get("/v1/api/datatables/certificados/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        row = data["data"][0]
        assert row["certificado_obra"] == "Obra Poliza Test"
        assert row["certificado_rubro_db"] == "Vivienda"

        resp = self.client.get("/v1/api/datatables/certificados/filtro-rubro/")
        assert [self.rubro.id, "Vivienda"] in resp.json()["choices"]


class IncorporacionDatatableTest(TestCase):
    def setUp(self):
        from carga.models import Provincia
        from personalizador.models import Agente, GeneroAgente
        from secretariador.models import (
            Incorporacion, InstrumentosLegalesDecretos, MontoViaticoDiario, Solicitud,
        )

        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.agente = Agente.objects.create(
            agente_nombres="Carla", agente_apellidos="Diaz", sexo=genero, dni=30555666, cuil="27305556669",
        )
        provincia = Provincia.objects.create(id=1, provincia_nombre="Chaco")
        decreto = InstrumentosLegalesDecretos.objects.create(
            instrumentolegaldecretos_numero="200", instrumentolegaldecretos_ano="2026",
        )
        monto_viatico = MontoViaticoDiario.objects.create(montoviaticodiario_decreto_reglamentario=decreto)
        solicitud = Solicitud.objects.create(
            solicitud_actuacion_ano=2026, solicitud_actuacion_numero=1, solicitud_solicitante=self.agente,
            solicitud_provincia=provincia, solicitud_decreto_viaticos=monto_viatico,
            solicitud_fecha_desde="2026-01-01", solicitud_fecha_hasta="2026-01-02",
            solicitud_tareas="tarea", solicitud_dia_inhabil=False,
        )
        self.incorporacion = Incorporacion.objects.create(
            incorporacion_actuacion_ano=2026, incorporacion_actuacion_numero=1,
            incorporacion_solicitud=solicitud, incorporacion_solicitante=self.agente,
        )

        self.user = UserModel.objects.create_user(username="incorp_user", password="pass1234!")
        self.client = Client()
        self.client.login(username="incorp_user", password="pass1234!")
        perm = Permission.objects.get(codename="view_incorporacion", content_type__app_label="secretariador")
        self.user.user_permissions.add(perm)

    def test_lists_rows(self):
        resp = self.client.get("/v1/api/datatables/incorporaciones/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["recordsTotal"] == 1
        row = data["data"][0]
        assert row["incorporacion_solicitante"] == "Carla Diaz"
        assert "E10-2026-1-AE" in row["incorporacion_solicitud"]


class InstrumentosLegalesDatatableTest(TestCase):
    def setUp(self):
        from secretariador.models import (
            InstrumentosLegalesDecretos, InstrumentosLegalesMemorandum, InstrumentosLegalesResoluciones,
        )

        self.memorandum = InstrumentosLegalesMemorandum.objects.create(
            instrumentolegalmemorandum_numero="1", instrumentolegalmemorandum_ano="2026",
            instrumentolegalmemorandum_descripcion="Memo test", instrumentolegalmemorandum_document="texto ocr " * 30,
        )
        self.decreto = InstrumentosLegalesDecretos.objects.create(
            instrumentolegaldecretos_numero="2", instrumentolegaldecretos_ano="2026",
        )
        self.resolucion_p = InstrumentosLegalesResoluciones.objects.create(
            instrumentolegalresoluciones_tipo="P", instrumentolegalresoluciones_numero="3",
            instrumentolegalresoluciones_ano="2026",
        )
        self.resolucion_d = InstrumentosLegalesResoluciones.objects.create(
            instrumentolegalresoluciones_tipo="D", instrumentolegalresoluciones_numero="4",
            instrumentolegalresoluciones_acta="10", instrumentolegalresoluciones_ano="2026",
        )

        self.user = UserModel.objects.create_user(username="instr_user", password="pass1234!")
        self.client = Client()
        self.client.login(username="instr_user", password="pass1234!")
        perm = Permission.objects.get(
            codename="view_instrumentoslegalesmemorandum", content_type__app_label="secretariador",
        )
        self.user.user_permissions.add(perm)
        perm = Permission.objects.get(
            codename="view_instrumentoslegalesdecretos", content_type__app_label="secretariador",
        )
        self.user.user_permissions.add(perm)
        perm = Permission.objects.get(
            codename="view_instrumentoslegalesresoluciones", content_type__app_label="secretariador",
        )
        self.user.user_permissions.add(perm)

    def test_memorandums_truncates_ocr_document(self):
        resp = self.client.get("/v1/api/datatables/memorandums/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert "&hellip;" in data["data"][0]["instrumentolegalmemorandum_document"]

    def test_decretos_uses_get_absolute_url_for_edit_link(self):
        resp = self.client.get("/v1/api/datatables/decretos/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert f"/viaticos/creardecreto/{self.decreto.id}" in data["data"][0]["acciones"] or \
            f"/{self.decreto.id}" in data["data"][0]["acciones"]

    def test_resoluciones_lists_both_tipos(self):
        resp = self.client.get("/v1/api/datatables/resoluciones/")
        data = resp.json()
        assert data["recordsTotal"] == 2
        tipos = {row["instrumentolegalresoluciones_tipo"] for row in data["data"]}
        assert tipos == {"Resolución de Presidencia", "Resolución de Directorio"}

    def test_resoluciones_directorio_only_lists_tipo_d(self):
        resp = self.client.get("/v1/api/datatables/resoluciones-directorio/")
        data = resp.json()
        assert data["recordsTotal"] == 1
        assert data["data"][0]["instrumentolegalresoluciones_acta"] == "10"
