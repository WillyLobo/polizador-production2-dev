import io
import zipfile
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from secretariador.docx_header import inject_header, tiene_encabezado_valido

UserModel = get_user_model()

BASE = Path(settings.BASE_DIR)
BODY_TEMPLATE = BASE / "secretariador/media/solicitud_template.docx"
HEADER_SOURCE = BASE / "secretariador/media/solicitud_exterior.docx"


def _read_part(docx_bytes, part):
    with zipfile.ZipFile(io.BytesIO(docx_bytes)) as zf:
        return zf.read(part)


def _build_header_docx_with_marker():
    """Copia solicitud_exterior.docx pero con un texto distinto en su header de primera página."""
    with open(HEADER_SOURCE, "rb") as f:
        original = f.read()
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(original)) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/header3.xml":
                assert b"Provincia del Chaco" in data
                data = data.replace(b"Provincia del Chaco", b"ENCABEZADO DE PRUEBA")
            zout.writestr(info, data)
    out.seek(0)
    return out


class InjectHeaderTests(TestCase):
    def test_header_is_replaced_and_body_untouched(self):
        original_body_document_xml = _read_part(BODY_TEMPLATE.read_bytes(), "word/document.xml")

        merged = inject_header(BODY_TEMPLATE, _build_header_docx_with_marker())
        merged_bytes = merged.read()

        merged_header = _read_part(merged_bytes, "word/header3.xml")
        self.assertIn(b"ENCABEZADO DE PRUEBA", merged_header)
        self.assertNotIn(b"Provincia del Chaco", merged_header)

        merged_document_xml = _read_part(merged_bytes, "word/document.xml")
        self.assertEqual(merged_document_xml, original_body_document_xml)
        self.assertIn(b"{{parrafo_uno}}", merged_document_xml)

    def test_tiene_encabezado_valido_true_for_real_template(self):
        with open(BODY_TEMPLATE, "rb") as f:
            self.assertTrue(tiene_encabezado_valido(f))

    def test_tiene_encabezado_valido_false_for_garbage(self):
        garbage = io.BytesIO(b"not a docx at all")
        self.assertFalse(tiene_encabezado_valido(garbage))


class ReportesCalendarioViewsTest(TestCase):
    """Las vistas de reportes/*.html ya no calculan los eventos: solo arman el shell
    y le pasan a FullCalendar la URL del endpoint de /v1/api/calendario/ con los
    filtros elegidos (ver secretariador/views/reportesviews.py)."""

    def setUp(self):
        from personalizador.models import Agente, GeneroAgente

        self.user = UserModel.objects.create_user(username="reportes_user", password="pass1234!")
        perm = Permission.objects.get(codename="view_solicitud", content_type__app_label="secretariador")
        self.user.user_permissions.add(perm)
        self.client.login(username="reportes_user", password="pass1234!")

        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.agente = Agente.objects.create(
            agente_nombres="Juan", agente_apellidos="Perez",
            sexo=genero, dni=30111222, cuil="20301112223",
        )

    def test_agente_individual_shell_without_filters(self):
        resp = self.client.get(reverse("secretariador:crear-reporte-viaticos-por-agente-individual"))
        self.assertEqual(resp.status_code, 200)
        # sin agente elegido no debe intentar pedir eventos
        self.assertNotIn("/v1/api/calendario/agente-individual/", resp.content.decode())

    def test_agente_individual_shell_with_filters_points_to_api(self):
        resp = self.client.get(
            reverse("secretariador:crear-reporte-viaticos-por-agente-individual"),
            {"agente": self.agente.id, "ano": 2025},
        )
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn("/v1/api/calendario/agente-individual/", content)
        self.assertIn(f"agente: '{self.agente.id}'", content)
        self.assertIn("ano: '2025'", content)
        self.assertIn("2025-01-01", content)

    def test_agente_individual_404_for_unknown_agente(self):
        resp = self.client.get(
            reverse("secretariador:crear-reporte-viaticos-por-agente-individual"),
            {"agente": 999999, "ano": 2025},
        )
        self.assertEqual(resp.status_code, 404)

    def test_calendario_anual_shell_points_to_api(self):
        resp = self.client.get(reverse("secretariador:calendario-anual"), {"ano": 2024})
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn("/v1/api/calendario/anual/", content)
        self.assertIn("ano: '2024'", content)
        self.assertIn("2024-01-01", content)

    def test_calendario_semanal_shell_without_agente(self):
        resp = self.client.get(reverse("secretariador:calendario-semanal"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn("/v1/api/calendario/semanal/", content)
        self.assertNotIn("extraParams", content)

    def test_calendario_semanal_shell_with_agente(self):
        resp = self.client.get(reverse("secretariador:calendario-semanal"), {"agente": self.agente.id})
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn(f"agente: '{self.agente.id}'", content)

    def test_calendario_anual_defaults_to_current_week_without_ano_filter(self):
        resp = self.client.get(reverse("secretariador:calendario-anual"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        hoy = datetime.today().strftime("%Y-%m-%d")
        self.assertIn(f'initialDate: "{hoy}"', content)

    def test_calendario_anual_ano_disponible_construido_desde_solicitudes(self):
        from carga.models import Provincia
        from secretariador.models import InstrumentosLegalesDecretos, MontoViaticoDiario, Solicitud

        provincia = Provincia.objects.create(id=1, provincia_nombre="Chaco")
        decreto = InstrumentosLegalesDecretos.objects.create(
            instrumentolegaldecretos_numero="100", instrumentolegaldecretos_ano="2026",
        )
        monto_viatico = MontoViaticoDiario.objects.create(montoviaticodiario_decreto_reglamentario=decreto)
        for ano, numero in [(2023, 1), (2026, 2)]:
            Solicitud.objects.create(
                solicitud_actuacion_ano=ano, solicitud_actuacion_numero=numero,
                solicitud_solicitante=self.agente, solicitud_provincia=provincia,
                solicitud_decreto_viaticos=monto_viatico,
                solicitud_fecha_desde=f"{ano}-03-01", solicitud_fecha_hasta=f"{ano}-03-02",
                solicitud_tareas="Tarea de prueba", solicitud_dia_inhabil=False,
            )

        resp = self.client.get(reverse("secretariador:calendario-anual"))
        content = resp.content.decode()
        self.assertIn('value="2023"', content)
        self.assertIn('value="2026"', content)
        self.assertNotIn('value="2099"', content)
