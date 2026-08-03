import io
import tempfile
import zipfile
import zlib
from datetime import date, datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
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


# --- Empaquetado vía GCS compose (gcs_zip.py) ---------------------------------
#
# compose() no está disponible sin credenciales/red reales (ya se probó en vivo
# contra el bucket de producción bajo un prefijo scratch, ver la conversación),
# así que estos tests usan un bucket/blob falsos que simulan compose() como una
# concatenación de bytes en memoria — exactamente lo que hace GCS — para poder
# validar de forma hermética y rápida que el ZIP resultante es válido.

class _BlobFalso:
    def __init__(self, store, name):
        self._store = store
        self.name = name
        self.content_type = None

    @property
    def size(self):
        return len(self._store[self.name])

    def reload(self):
        pass

    def exists(self):
        return self.name in self._store

    def upload_from_string(self, data, content_type=None):
        self._store[self.name] = data
        self.content_type = content_type

    def compose(self, sources):
        self._store[self.name] = b"".join(self._store[s.name] for s in sources)

    def delete(self):
        self._store.pop(self.name, None)


class _ListaBlobsFalsa(list):
    """Imita el HTTPIterator que devuelve bucket.list_blobs(): iterable de
    blobs, con .prefixes poblado cuando se pide delimiter (simulando un
    listado "por carpetas", como hace la API real de GCS)."""

    def __init__(self, blobs, prefixes=()):
        super().__init__(blobs)
        self.prefixes = set(prefixes)


class _BucketFalso:
    def __init__(self):
        self.store = {}

    def blob(self, name):
        return _BlobFalso(self.store, name)

    def set_content(self, name, content):
        self.store[name] = content

    def list_blobs(self, prefix="", delimiter=None):
        nombres = sorted(n for n in self.store if n.startswith(prefix))
        if delimiter is None:
            return _ListaBlobsFalsa(self.blob(n) for n in nombres)

        prefijos = set()
        blobs_directos = []
        for nombre in nombres:
            resto = nombre[len(prefix):]
            if delimiter in resto:
                subcarpeta = resto.split(delimiter, 1)[0]
                prefijos.add(f"{prefix}{subcarpeta}{delimiter}")
            else:
                blobs_directos.append(self.blob(nombre))
        return _ListaBlobsFalsa(blobs_directos, prefixes=prefijos)


class GCSZipComposerTest(TestCase):
    """Prueba secretariador/gcs_zip.py sin tocar GCS de verdad: el bucket falso
    implementa compose() como concatenación de bytes en memoria, que es
    exactamente lo que hace la API real, así que ejercita el mismo código
    (incluido el árbol de reducción cuando hay más de 32 fuentes)."""

    def setUp(self):
        self.bucket = _BucketFalso()

    def _crear_entrada(self, nombre, contenido):
        from secretariador.gcs_zip import EntradaZip

        blob = self.bucket.blob(f"instrumentoslegales/resoluciones/{nombre}")
        self.bucket.set_content(blob.name, contenido)
        return EntradaZip(
            nombre_archivo=nombre, tamano=len(contenido), crc32=zlib.crc32(contenido), blob_origen=blob,
            date_time=(2026, 3, 5, 0, 0, 0),
        )

    def test_componer_zip_simple(self):
        from secretariador.gcs_zip import componer_zip, limpiar_temporales

        entradas = [
            self._crear_entrada("1-2026-P.pdf", b"contenido de la primera resolucion"),
            self._crear_entrada("2-2026-P.pdf", b"contenido de la segunda resolucion, mas largo"),
        ]

        destino, temporales = componer_zip(self.bucket, entradas, "paquetes/destino.zip", "scratch")

        with zipfile.ZipFile(io.BytesIO(self.bucket.store[destino.name])) as zf:
            self.assertIsNone(zf.testzip())
            self.assertEqual(zf.namelist(), ["1-2026-P.pdf", "2-2026-P.pdf"])
            self.assertEqual(zf.read("1-2026-P.pdf"), b"contenido de la primera resolucion")
            self.assertEqual(zf.read("2-2026-P.pdf"), b"contenido de la segunda resolucion, mas largo")

        limpiar_temporales(temporales)
        # Los headers, el directorio central y los intermedios de compose se
        # borraron; el destino y los blobs originales de las resoluciones
        # (nunca están en `temporales`) siguen ahí.
        self.assertEqual(
            set(self.bucket.store.keys()),
            {destino.name, *(e.blob_origen.name for e in entradas)},
        )

    def test_componer_zip_con_mas_de_32_fuentes_usa_arbol_de_compose(self):
        from secretariador.gcs_zip import MAX_FUENTES_POR_COMPOSE, componer_zip

        # 40 entradas -> 2*40 + 1 (directorio central) = 81 piezas, fuerza más
        # de una ronda del árbol de reducción (límite de 32 fuentes/compose).
        cantidad = 40
        self.assertGreater(2 * cantidad + 1, MAX_FUENTES_POR_COMPOSE)
        entradas = [
            self._crear_entrada(f"{i:02d}-2026-P.pdf", f"contenido resolucion {i}".encode())
            for i in range(cantidad)
        ]

        destino, _temporales = componer_zip(self.bucket, entradas, "paquetes/destino.zip", "scratch")

        with zipfile.ZipFile(io.BytesIO(self.bucket.store[destino.name])) as zf:
            self.assertIsNone(zf.testzip())
            # El orden de las entradas en el zip tiene que sobrevivir al árbol
            # de reducción, no solo el conjunto.
            self.assertEqual(zf.namelist(), [f"{i:02d}-2026-P.pdf" for i in range(cantidad)])
            for i, entrada in enumerate(entradas):
                self.assertEqual(zf.read(entrada.nombre_archivo), f"contenido resolucion {i}".encode())

    def test_nombre_no_ascii_lanza_error_antes_de_componer(self):
        from secretariador.gcs_zip import componer_zip

        entrada = self._crear_entrada("año-2026-P.pdf", b"contenido")
        with self.assertRaises(ValueError):
            componer_zip(self.bucket, [entrada], "paquetes/destino.zip", "scratch")


class EmpaquetarResolucionesMensualCommandTest(TestCase):
    """Pruebas de la lógica pura del comando de cron (sin tocar GCS)."""

    def test_mes_anterior_dentro_del_mismo_ano(self):
        from secretariador.management.commands.empaquetar_resoluciones_mensual import _mes_anterior

        self.assertEqual(_mes_anterior(date(2026, 8, 3)), (2026, 7))

    def test_mes_anterior_cruzando_ano(self):
        from secretariador.management.commands.empaquetar_resoluciones_mensual import _mes_anterior

        self.assertEqual(_mes_anterior(date(2026, 1, 15)), (2025, 12))

    def test_armar_paquetes_agrupa_respetando_tamano_maximo(self):
        from secretariador.gcs_zip import EntradaZip
        from secretariador.management.commands.empaquetar_resoluciones_mensual import _armar_paquetes

        entradas = [
            EntradaZip(nombre_archivo=f"{i}.pdf", tamano=10, crc32=0, blob_origen=None)
            for i in range(5)
        ]

        paquetes = _armar_paquetes(entradas, tamano_maximo=25)

        self.assertEqual([len(p) for p in paquetes], [2, 2, 1])

    def test_armar_paquetes_entrada_mas_grande_que_el_maximo_queda_sola(self):
        from secretariador.gcs_zip import EntradaZip
        from secretariador.management.commands.empaquetar_resoluciones_mensual import _armar_paquetes

        # El algoritmo es secuencial (no reordena por tamaño para optimizar el
        # packing): "gigante" fuerza su propio paquete y corta la racha, así
        # que "otra_chica" no se puede agrupar con "chica" aunque ambas entren
        # holgadas en el límite.
        entradas = [
            EntradaZip(nombre_archivo="chica.pdf", tamano=5, crc32=0, blob_origen=None),
            EntradaZip(nombre_archivo="gigante.pdf", tamano=100, crc32=0, blob_origen=None),
            EntradaZip(nombre_archivo="otra_chica.pdf", tamano=5, crc32=0, blob_origen=None),
        ]

        paquetes = _armar_paquetes(entradas, tamano_maximo=10)

        self.assertEqual([[e.nombre_archivo for e in p] for p in paquetes], [
            ["chica.pdf"], ["gigante.pdf"], ["otra_chica.pdf"],
        ])


class ListarPaquetesResolucionesTest(TestCase):
    """Prueba secretariador/views/paqueteresolucionesviews.py::_listar_meses
    (lectura pura de la estructura de carpetas, sin tocar GCS de verdad)."""

    def setUp(self):
        self.bucket = _BucketFalso()

    def _agregar_paquete(self, ano, mes, indice, tamano):
        from secretariador.views.paqueteresolucionesviews import DESTINO_PREFIJO

        nombre = f"{DESTINO_PREFIJO}/{ano}-{mes:02d}/paquete-{indice:02d}.zip"
        self.bucket.set_content(nombre, b"x" * tamano)

    def test_agrupa_por_ano_mes_y_ordena_los_mas_recientes_primero(self):
        from secretariador.views.paqueteresolucionesviews import _listar_meses

        self._agregar_paquete(2026, 6, 1, tamano=10)
        self._agregar_paquete(2026, 8, 1, tamano=20)
        self._agregar_paquete(2026, 8, 2, tamano=30)

        meses = _listar_meses(self.bucket)

        self.assertEqual([(m["ano"], m["mes"]) for m in meses], [(2026, 8), (2026, 6)])
        agosto = meses[0]
        self.assertEqual(agosto["nombre_mes"], "Agosto")
        self.assertEqual(
            [(p["indice"], p["tamano"]) for p in agosto["paquetes"]],
            [(1, 20), (2, 30)],
        )

    def test_ignora_blobs_de_scratch_que_no_terminan_en_zip(self):
        from secretariador.views.paqueteresolucionesviews import DESTINO_PREFIJO, _listar_meses

        self._agregar_paquete(2026, 8, 1, tamano=20)
        self.bucket.set_content(f"{DESTINO_PREFIJO}/2026-08/_scratch/header-0", b"basura")

        meses = _listar_meses(self.bucket)

        self.assertEqual(len(meses), 1)
        self.assertEqual(len(meses[0]["paquetes"]), 1)

    def test_no_hay_paquetes(self):
        from secretariador.views.paqueteresolucionesviews import _listar_meses

        self.assertEqual(_listar_meses(self.bucket), [])


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class ResolucionCrc32SignalTest(TestCase):
    """El signal en secretariador/signals.py tiene que cachear el CRC-32 (el
    mismo algoritmo que usa el formato ZIP, no el CRC32C que calcula GCS solo)
    apenas se sube un archivo nuevo — es lo que le permite a
    empaquetar_resoluciones_mensual armar los ZIPs sin releer los PDFs."""

    def setUp(self):
        media_root_override = override_settings(MEDIA_ROOT=tempfile.mkdtemp())
        media_root_override.enable()
        self.addCleanup(media_root_override.disable)

    def test_crc32_se_calcula_al_subir_un_archivo_nuevo(self):
        from secretariador.models import InstrumentosLegalesResoluciones

        contenido = b"%PDF-1.4 contenido de prueba para el signal"
        resolucion = InstrumentosLegalesResoluciones.objects.create(
            instrumentolegalresoluciones_tipo="P", instrumentolegalresoluciones_numero="1",
            instrumentolegalresoluciones_ano="2026",
            instrumentolegalresoluciones=SimpleUploadedFile("r1.pdf", contenido, content_type="application/pdf"),
        )

        self.assertEqual(resolucion.instrumentolegalresoluciones_crc32, zlib.crc32(contenido))

    def test_no_recalcula_si_se_guarda_sin_tocar_el_archivo(self):
        from secretariador.models import InstrumentosLegalesResoluciones

        resolucion = InstrumentosLegalesResoluciones.objects.create(
            instrumentolegalresoluciones_tipo="P", instrumentolegalresoluciones_numero="2",
            instrumentolegalresoluciones_ano="2026",
            instrumentolegalresoluciones=SimpleUploadedFile("r2.pdf", b"contenido original", content_type="application/pdf"),
        )
        crc_original = resolucion.instrumentolegalresoluciones_crc32

        resolucion.instrumentolegalresoluciones_descripcion = "actualizado"
        resolucion.save(update_fields=["instrumentolegalresoluciones_descripcion"])

        resolucion.refresh_from_db()
        self.assertEqual(resolucion.instrumentolegalresoluciones_crc32, crc_original)
