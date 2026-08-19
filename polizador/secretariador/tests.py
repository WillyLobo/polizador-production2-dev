import io
import tempfile
import zipfile
from datetime import date, datetime
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


class ValorViaticoDiaTests(TestCase):
    """Prueba ComisionadoSolicitud.valor_viatico_dia() (secretariador/models.py),
    incluyendo las reglas configurables en ReglasViatico (gabinete, autoridades del
    Directorio, escalafón único forzado) que reemplazan al viejo estrato=2 fijo."""

    def setUp(self):
        from carga.models import Provincia
        from personalizador.models import Agente, ComisionadoExterno, Directorio, GeneroAgente
        from secretariador.models import (
            ComisionadoSolicitud, InstrumentosLegalesDecretos, MontoViaticoDiario,
            ReglasViatico, Solicitud,
        )

        self.ComisionadoSolicitud = ComisionadoSolicitud
        self.ReglasViatico = ReglasViatico

        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.provincia_chaco = Provincia.objects.create(id=1, provincia_nombre="Chaco")
        self.provincia_otra = Provincia.objects.create(id=2, provincia_nombre="Corrientes")

        decreto = InstrumentosLegalesDecretos.objects.create(
            instrumentolegaldecretos_numero="1", instrumentolegaldecretos_ano="2026",
        )
        self.monto = MontoViaticoDiario.objects.create(
            montoviaticodiario_decreto_reglamentario=decreto,
            montoviaticodiario_estrato_uno_interior=10, montoviaticodiario_estrato_dos_interior=20,
            montoviaticodiario_estrato_tres_interior=30, montoviaticodiario_estrato_cuatro_interior=40,
            montoviaticodiario_estrato_uno_exterior=100, montoviaticodiario_estrato_dos_exterior=200,
            montoviaticodiario_estrato_tres_exterior=300, montoviaticodiario_estrato_cuatro_exterior=400,
        )

        self.solicitante = Agente.objects.create(
            agente_nombres="Solicitante", agente_apellidos="Test",
            sexo=genero, dni=30000001, cuil="20300000013",
        )
        self.agente_normal = Agente.objects.create(
            agente_nombres="Normal", agente_apellidos="Test",
            sexo=genero, dni=30000002, cuil="20300000023",
        )
        self.agente_gabinete = Agente.objects.create(
            agente_nombres="Gabinete", agente_apellidos="Test",
            sexo=genero, dni=30000003, cuil="20300000033", agente_personal_de_gabinete=True,
        )
        self.agente_autoridad = Agente.objects.create(
            agente_nombres="Autoridad", agente_apellidos="Test",
            sexo=genero, dni=30000004, cuil="20300000043",
        )
        Directorio.objects.create(
            directorio_nombre="Presidencia", directorio_cuof="001",
            directorio_autoridad_a_cargo_fk=self.agente_autoridad,
        )
        self.externo = ComisionadoExterno.objects.create(
            agente_nombres="Externo", agente_apellidos="Test",
            sexo=genero, dni=30000005, cuil="20300000053",
        )
        self._solicitud_numero = 0

    def _comisionado(self, provincia, agente=None, externo=None, **kwargs):
        self._solicitud_numero += 1
        solicitud = self.Solicitud.objects.create(
            solicitud_actuacion_ano=2026, solicitud_actuacion_numero=self._solicitud_numero,
            solicitud_solicitante=self.solicitante, solicitud_provincia=provincia,
            solicitud_decreto_viaticos=self.monto,
            solicitud_fecha_desde="2026-01-01", solicitud_fecha_hasta="2026-01-02",
            solicitud_tareas="Tarea de prueba", solicitud_dia_inhabil=False,
        )
        kwargs.setdefault("comisionadosolicitud_colaborador", False)
        kwargs.setdefault("comisionadosolicitud_chofer", False)
        return self.ComisionadoSolicitud(
            comisionadosolicitud_foreign=solicitud,
            comisionadosolicitud_nombre=agente, comisionadosolicitud_externo=externo,
            **kwargs,
        )

    @property
    def Solicitud(self):
        from secretariador.models import Solicitud
        return Solicitud

    def test_agente_normal_usa_escalafon_por_defecto_dos(self):
        comisionado = self._comisionado(self.provincia_chaco, agente=self.agente_normal)
        self.assertEqual(comisionado.valor_viatico_dia(), self.monto.montoviaticodiario_estrato_dos_interior)

    def test_agente_normal_con_escalafon_explicito(self):
        self.agente_normal.agente_escalafon = 3
        self.agente_normal.save()
        comisionado = self._comisionado(self.provincia_otra, agente=self.agente_normal)
        self.assertEqual(comisionado.valor_viatico_dia(), self.monto.montoviaticodiario_estrato_tres_exterior)

    def test_gabinete_no_cobra_por_defecto(self):
        comisionado = self._comisionado(self.provincia_chaco, agente=self.agente_gabinete)
        self.assertEqual(comisionado.valor_viatico_dia(), 0)

    def test_gabinete_cobra_si_la_regla_lo_habilita(self):
        reglas = self.ReglasViatico.get_solo()
        reglas.reglas_gabinete_cobra_viatico = True
        reglas.save()
        comisionado = self._comisionado(self.provincia_chaco, agente=self.agente_gabinete)
        self.assertEqual(comisionado.valor_viatico_dia(), self.monto.montoviaticodiario_estrato_dos_interior)

    def test_autoridad_no_cobra_dentro_de_chaco_por_defecto(self):
        comisionado = self._comisionado(self.provincia_chaco, agente=self.agente_autoridad)
        self.assertEqual(comisionado.valor_viatico_dia(), 0)

    def test_autoridad_cobra_estrato_cuatro_fuera_de_chaco(self):
        comisionado = self._comisionado(self.provincia_otra, agente=self.agente_autoridad)
        self.assertEqual(comisionado.valor_viatico_dia(), self.monto.montoviaticodiario_estrato_cuatro_exterior)

    def test_autoridad_cobra_dentro_de_chaco_si_la_regla_lo_habilita(self):
        reglas = self.ReglasViatico.get_solo()
        reglas.reglas_autoridades_cobra_viatico_chaco = True
        reglas.save()
        comisionado = self._comisionado(self.provincia_chaco, agente=self.agente_autoridad)
        self.assertEqual(comisionado.valor_viatico_dia(), self.monto.montoviaticodiario_estrato_cuatro_interior)

    def test_comisionado_externo_usa_escalafon_default_de_externos(self):
        comisionado = self._comisionado(self.provincia_chaco, externo=self.externo)
        self.assertEqual(comisionado.valor_viatico_dia(), self.monto.montoviaticodiario_estrato_dos_interior)

    def test_comisionado_externo_no_cobra_si_la_regla_lo_deshabilita(self):
        reglas = self.ReglasViatico.get_solo()
        reglas.reglas_externos_cobra_viatico = False
        reglas.save()
        comisionado = self._comisionado(self.provincia_chaco, externo=self.externo)
        self.assertEqual(comisionado.valor_viatico_dia(), 0)

    def test_escalafon_unico_forzado_pisa_todo_incluido_externos_y_autoridades(self):
        reglas = self.ReglasViatico.get_solo()
        reglas.reglas_escalafon_unico_habilitado = True
        reglas.reglas_escalafon_unico_valor = 1
        reglas.reglas_gabinete_cobra_viatico = True
        reglas.reglas_autoridades_cobra_viatico_chaco = True
        reglas.save()
        for kwargs in (
            {"agente": self.agente_normal}, {"agente": self.agente_gabinete},
            {"agente": self.agente_autoridad}, {"externo": self.externo},
        ):
            with self.subTest(**kwargs):
                comisionado = self._comisionado(self.provincia_chaco, **kwargs)
                self.assertEqual(
                    comisionado.valor_viatico_dia(), self.monto.montoviaticodiario_estrato_uno_interior,
                )

    def test_colaborador_no_cobra_sin_importar_escalafon(self):
        comisionado = self._comisionado(self.provincia_chaco, agente=self.agente_normal, comisionadosolicitud_colaborador=True)
        self.assertEqual(comisionado.valor_viatico_dia(), 0)


# --- Empaquetado de resoluciones (paquetes_resoluciones.py) -------------------
#
# armar_zip/armar_pdf son lógica pura (reciben bytes ya leídos, en memoria) así
# que se prueban directo, sin bucket ni disco falsos. Los tests de _listar_meses
# sí necesitan un bucket falso, porque esa función lista blobs de verdad.

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


class ArmarPaquetesResolucionesTest(TestCase):
    """Prueba secretariador/paquetes_resoluciones.py: armar_zip/armar_pdf son
    lógica pura (reciben bytes ya leídos), y leer_contenido prioriza el disco
    local sobre bajar de GCS."""

    def _entrada_local(self, tmp_path, nombre, contenido, date_time=(2026, 3, 5, 0, 0, 0)):
        from secretariador.paquetes_resoluciones import EntradaResolucion

        ruta = tmp_path / nombre
        ruta.write_bytes(contenido)
        return EntradaResolucion(
            nombre_archivo=nombre, tamano=len(contenido), date_time=date_time, ruta_local=ruta,
        )

    def test_armar_zip_incluye_las_entradas_en_orden_y_es_valido(self):
        from secretariador.paquetes_resoluciones import armar_zip

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            entradas = [
                self._entrada_local(tmp_path, "1-2026-P.pdf", b"contenido de la primera resolucion"),
                self._entrada_local(tmp_path, "2-2026-P.pdf", b"contenido de la segunda resolucion, mas largo"),
            ]

            with zipfile.ZipFile(io.BytesIO(armar_zip(entradas))) as zf:
                self.assertIsNone(zf.testzip())
                self.assertEqual(zf.namelist(), ["1-2026-P.pdf", "2-2026-P.pdf"])
                self.assertEqual(zf.read("1-2026-P.pdf"), b"contenido de la primera resolucion")
                self.assertEqual(zf.read("2-2026-P.pdf"), b"contenido de la segunda resolucion, mas largo")

    def test_armar_zip_soporta_nombres_no_ascii(self):
        # A diferencia del viejo armado vía compose() de bytes (que exigía
        # nombres ASCII porque no seteaba el flag UTF-8), zipfile lo maneja solo.
        from secretariador.paquetes_resoluciones import armar_zip

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            entradas = [self._entrada_local(tmp_path, "año-2026-P.pdf", b"contenido")]

            with zipfile.ZipFile(io.BytesIO(armar_zip(entradas))) as zf:
                self.assertIsNone(zf.testzip())
                self.assertEqual(zf.namelist(), ["año-2026-P.pdf"])

    def test_armar_pdf_fusiona_las_paginas_de_todas_las_entradas(self):
        import pikepdf
        from secretariador.paquetes_resoluciones import armar_pdf

        def _pdf_de_n_paginas(n):
            pdf = pikepdf.new()
            for _ in range(n):
                pdf.add_blank_page(page_size=(72, 72))
            buffer = io.BytesIO()
            pdf.save(buffer)
            return buffer.getvalue()

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            entradas = [
                self._entrada_local(tmp_path, "1-2026-P.pdf", _pdf_de_n_paginas(2)),
                self._entrada_local(tmp_path, "2-2026-P.pdf", _pdf_de_n_paginas(3)),
            ]

            resultado = armar_pdf(entradas)

        with pikepdf.open(io.BytesIO(resultado)) as pdf:
            self.assertEqual(len(pdf.pages), 5)

    def test_leer_contenido_prioriza_disco_local_sobre_gcs(self):
        from secretariador.paquetes_resoluciones import EntradaResolucion, leer_contenido

        class _BlobQueExplotaSiSeLee:
            def download_as_bytes(self):
                raise AssertionError("no debería bajar de GCS si el archivo está en disco local")

        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "resolucion.pdf"
            ruta.write_bytes(b"contenido local")
            entrada = EntradaResolucion(
                nombre_archivo="resolucion.pdf", tamano=len(b"contenido local"),
                date_time=(2026, 3, 5, 0, 0, 0), ruta_local=ruta, blob_origen=_BlobQueExplotaSiSeLee(),
            )
            self.assertEqual(leer_contenido(entrada), b"contenido local")

    def test_leer_contenido_baja_de_gcs_si_no_esta_en_disco_local(self):
        from secretariador.paquetes_resoluciones import EntradaResolucion, leer_contenido

        class _BlobFalsoConContenido:
            def download_as_bytes(self):
                return b"contenido de gcs"

        entrada = EntradaResolucion(
            nombre_archivo="resolucion.pdf", tamano=16, date_time=(2026, 3, 5, 0, 0, 0),
            ruta_local=None, blob_origen=_BlobFalsoConContenido(),
        )
        self.assertEqual(leer_contenido(entrada), b"contenido de gcs")


class EmpaquetarResolucionesMensualCommandTest(TestCase):
    """Pruebas de la lógica pura del comando de cron (sin tocar GCS)."""

    def test_mes_anterior_dentro_del_mismo_ano(self):
        from secretariador.paquetes_resoluciones import mes_anterior

        self.assertEqual(mes_anterior(date(2026, 8, 3)), (2026, 7))

    def test_mes_anterior_cruzando_ano(self):
        from secretariador.paquetes_resoluciones import mes_anterior

        self.assertEqual(mes_anterior(date(2026, 1, 15)), (2025, 12))

    def test_armar_paquetes_agrupa_respetando_tamano_maximo(self):
        from secretariador.paquetes_resoluciones import EntradaResolucion, armar_paquetes

        entradas = [
            EntradaResolucion(nombre_archivo=f"{i}.pdf", tamano=10, date_time=(2026, 3, 5, 0, 0, 0))
            for i in range(5)
        ]

        paquetes = armar_paquetes(entradas, tamano_maximo=25)

        self.assertEqual([len(p) for p in paquetes], [2, 2, 1])

    def test_armar_paquetes_entrada_mas_grande_que_el_maximo_queda_sola(self):
        from secretariador.paquetes_resoluciones import EntradaResolucion, armar_paquetes

        # El algoritmo es secuencial (no reordena por tamaño para optimizar el
        # packing): "gigante" fuerza su propio paquete y corta la racha, así
        # que "otra_chica" no se puede agrupar con "chica" aunque ambas entren
        # holgadas en el límite.
        entradas = [
            EntradaResolucion(nombre_archivo="chica.pdf", tamano=5, date_time=(2026, 3, 5, 0, 0, 0)),
            EntradaResolucion(nombre_archivo="gigante.pdf", tamano=100, date_time=(2026, 3, 5, 0, 0, 0)),
            EntradaResolucion(nombre_archivo="otra_chica.pdf", tamano=5, date_time=(2026, 3, 5, 0, 0, 0)),
        ]

        paquetes = armar_paquetes(entradas, tamano_maximo=10)

        self.assertEqual([[e.nombre_archivo for e in p] for p in paquetes], [
            ["chica.pdf"], ["gigante.pdf"], ["otra_chica.pdf"],
        ])


class ListarPaquetesResolucionesTest(TestCase):
    """Prueba secretariador/views/paqueteresolucionesviews.py::_listar_meses
    (lectura pura de la estructura de carpetas, sin tocar GCS de verdad)."""

    def setUp(self):
        self.bucket = _BucketFalso()

    def _agregar_paquete(self, ano, mes, indice, tamano, extension=".zip"):
        from secretariador.views.paqueteresolucionesviews import DESTINO_PREFIJO

        nombre = f"{DESTINO_PREFIJO}/{ano}-{mes:02d}/paquete-{indice:02d}{extension}"
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
            [(p["indice"], p["tamano"]) for p in agosto["formatos"]["zip"]],
            [(1, 20), (2, 30)],
        )

    def test_lista_zip_y_pdf_por_separado_cuando_ambos_existen(self):
        from secretariador.views.paqueteresolucionesviews import _listar_meses

        self._agregar_paquete(2026, 8, 1, tamano=20, extension=".zip")
        self._agregar_paquete(2026, 8, 1, tamano=15, extension=".pdf")

        meses = _listar_meses(self.bucket)

        self.assertEqual(len(meses), 1)
        self.assertEqual([(p["indice"], p["tamano"]) for p in meses[0]["formatos"]["zip"]], [(1, 20)])
        self.assertEqual([(p["indice"], p["tamano"]) for p in meses[0]["formatos"]["pdf"]], [(1, 15)])

    def test_ignora_blobs_de_scratch_que_no_terminan_en_zip_o_pdf(self):
        from secretariador.views.paqueteresolucionesviews import DESTINO_PREFIJO, _listar_meses

        self._agregar_paquete(2026, 8, 1, tamano=20)
        self.bucket.set_content(f"{DESTINO_PREFIJO}/2026-08/_scratch/header-0", b"basura")

        meses = _listar_meses(self.bucket)

        self.assertEqual(len(meses), 1)
        self.assertEqual(len(meses[0]["formatos"]["zip"]), 1)
        self.assertNotIn("pdf", meses[0]["formatos"])

    def test_no_hay_paquetes(self):
        from secretariador.views.paqueteresolucionesviews import _listar_meses

        self.assertEqual(_listar_meses(self.bucket), [])


class InvalidarTextoActuacionSignalsTestMixin:
    """Fixtures comunes para probar `secretariador/signals.py`: que editar los
    datos de una Solicitud/Incorporacion invalide el `*_texto_actuacion`
    guardado a mano, para que `editar_texto_solicitud`/`editar_texto_incorporacion`
    (y la generación del .docx) recalculen el texto en vez de mostrar uno
    desactualizado (ver `revisar_texto_actuacion` en textoactuacionviews.py)."""

    def setUp(self):
        from carga.models import Departamento, Localidad, Municipio, Provincia
        from personalizador.models import Agente, GeneroAgente
        from secretariador.models import (
            ComisionadoSolicitud, Incorporacion, InstrumentosLegalesDecretos,
            InstrumentosLegalesResoluciones, MontoViaticoDiario, Solicitud,
        )

        self.Solicitud = Solicitud
        self.Incorporacion = Incorporacion
        self.ComisionadoSolicitud = ComisionadoSolicitud

        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.provincia = Provincia.objects.create(id=1, provincia_nombre="Chaco")
        depto = Departamento.objects.create(id=1, departamento_nombre="Depto Test")
        municipio = Municipio.objects.create(id=1, municipio_nombre="Municipio Test", municipio_departamento=depto)
        self.localidad = Localidad.objects.create(
            id=1, localidad_nombre="Resistencia", localidad_departamento=depto, localidad_municipio=municipio,
        )

        decreto = InstrumentosLegalesDecretos.objects.create(
            instrumentolegaldecretos_numero="1", instrumentolegaldecretos_ano="2026",
        )
        self.monto = MontoViaticoDiario.objects.create(
            montoviaticodiario_decreto_reglamentario=decreto,
            montoviaticodiario_estrato_uno_interior=10, montoviaticodiario_estrato_dos_interior=20,
            montoviaticodiario_estrato_tres_interior=30, montoviaticodiario_estrato_cuatro_interior=40,
            montoviaticodiario_estrato_uno_exterior=100, montoviaticodiario_estrato_dos_exterior=200,
            montoviaticodiario_estrato_tres_exterior=300, montoviaticodiario_estrato_cuatro_exterior=400,
        )
        self.solicitante = Agente.objects.create(
            agente_nombres="Solicitante", agente_apellidos="Test", sexo=genero, dni=30000001, cuil="20300000013",
        )
        self.agente = Agente.objects.create(
            agente_nombres="Normal", agente_apellidos="Test", sexo=genero, dni=30000002, cuil="20300000023",
        )
        self.resolucion = InstrumentosLegalesResoluciones.objects.create(
            instrumentolegalresoluciones_numero=1, instrumentolegalresoluciones_ano="2026",
        )
        self.otra_resolucion = InstrumentosLegalesResoluciones.objects.create(
            instrumentolegalresoluciones_numero=2, instrumentolegalresoluciones_ano="2026",
        )

        self.solicitud = self.Solicitud.objects.create(
            solicitud_actuacion_ano=2026, solicitud_actuacion_numero=1,
            solicitud_solicitante=self.solicitante, solicitud_provincia=self.provincia,
            solicitud_decreto_viaticos=self.monto,
            solicitud_fecha_desde="2026-01-01", solicitud_fecha_hasta="2026-01-02",
            solicitud_tareas="Tarea de prueba", solicitud_dia_inhabil=False,
            solicitud_resolucion=self.resolucion,
            solicitud_texto_actuacion={"parrafos": ["viejo"], "articulo_uno": "viejo", "articulo_dos": []},
        )


class InvalidarTextoSolicitudTest(InvalidarTextoActuacionSignalsTestMixin, TestCase):
    def test_cambiar_fecha_invalida_texto_guardado(self):
        self.solicitud.solicitud_fecha_hasta = "2026-01-05"
        self.solicitud.save()
        self.solicitud.refresh_from_db()
        self.assertIsNone(self.solicitud.solicitud_texto_actuacion)

    def test_guardar_solo_el_texto_no_lo_invalida(self):
        self.solicitud.solicitud_texto_actuacion = {"parrafos": ["nuevo"], "articulo_uno": "nuevo", "articulo_dos": []}
        self.solicitud.save(update_fields=["solicitud_texto_actuacion"])
        self.solicitud.refresh_from_db()
        self.assertEqual(self.solicitud.solicitud_texto_actuacion["parrafos"], ["nuevo"])

    def test_agregar_comisionado_invalida_texto_guardado(self):
        self.ComisionadoSolicitud.objects.create(
            comisionadosolicitud_foreign=self.solicitud, comisionadosolicitud_nombre=self.agente,
            comisionadosolicitud_colaborador=False, comisionadosolicitud_chofer=False,
        )
        self.solicitud.refresh_from_db()
        self.assertIsNone(self.solicitud.solicitud_texto_actuacion)

    def test_borrar_comisionado_invalida_texto_guardado(self):
        com = self.ComisionadoSolicitud.objects.create(
            comisionadosolicitud_foreign=self.solicitud, comisionadosolicitud_nombre=self.agente,
            comisionadosolicitud_colaborador=False, comisionadosolicitud_chofer=False,
        )
        # repoblar el texto guardado, ya que crear el comisionado lo invalidó
        self.solicitud.solicitud_texto_actuacion = {"parrafos": ["viejo"], "articulo_uno": "viejo", "articulo_dos": []}
        self.solicitud.save(update_fields=["solicitud_texto_actuacion"])

        com.delete()
        self.solicitud.refresh_from_db()
        self.assertIsNone(self.solicitud.solicitud_texto_actuacion)

    def test_agregar_localidad_invalida_texto_guardado(self):
        self.solicitud.solicitud_localidades.add(self.localidad)
        self.solicitud.refresh_from_db()
        self.assertIsNone(self.solicitud.solicitud_texto_actuacion)

    def test_cambiar_resolucion_no_invalida_texto_propio_de_la_solicitud(self):
        """`solicitud_resolucion` no se usa en `_calcular_texto_solicitud`, solo
        en `_calcular_texto_incorporacion` de una Incorporacion asociada."""
        self.solicitud.solicitud_resolucion = self.otra_resolucion
        self.solicitud.save()
        self.solicitud.refresh_from_db()
        self.assertIsNotNone(self.solicitud.solicitud_texto_actuacion)


class InvalidarTextoIncorporacionTest(InvalidarTextoActuacionSignalsTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.incorporacion = self.Incorporacion.objects.create(
            incorporacion_solicitud=self.solicitud,
            incorporacion_actuacion_ano=2026, incorporacion_actuacion_numero=1,
            incorporacion_solicitante=self.solicitante,
            incorporacion_texto_actuacion={"parrafos": ["viejo"], "articulo_uno": "viejo", "articulo_dos": []},
        )

    def test_cambiar_numero_de_actuacion_propio_invalida_su_texto(self):
        self.incorporacion.incorporacion_actuacion_numero = 2
        self.incorporacion.save()
        self.incorporacion.refresh_from_db()
        self.assertIsNone(self.incorporacion.incorporacion_texto_actuacion)

    def test_cambiar_resolucion_de_la_solicitud_invalida_texto_de_incorporacion(self):
        """`solicitud_resolucion` sí se usa en `_calcular_texto_incorporacion`
        (vía `actuacion.incorporacion_solicitud.solicitud_resolucion`)."""
        self.solicitud.solicitud_resolucion = self.otra_resolucion
        self.solicitud.save()
        self.incorporacion.refresh_from_db()
        self.assertIsNone(self.incorporacion.incorporacion_texto_actuacion)

    def test_cambiar_fecha_de_la_solicitud_invalida_texto_de_incorporacion(self):
        self.solicitud.solicitud_fecha_hasta = "2026-01-05"
        self.solicitud.save()
        self.incorporacion.refresh_from_db()
        self.assertIsNone(self.incorporacion.incorporacion_texto_actuacion)

    def test_agregar_localidad_a_la_solicitud_invalida_texto_de_incorporacion(self):
        self.solicitud.solicitud_localidades.add(self.localidad)
        self.incorporacion.refresh_from_db()
        self.assertIsNone(self.incorporacion.incorporacion_texto_actuacion)

    def test_agregar_agente_a_la_solicitud_invalida_texto_de_incorporacion(self):
        self.ComisionadoSolicitud.objects.create(
            comisionadosolicitud_foreign=self.solicitud, comisionadosolicitud_nombre=self.agente,
            comisionadosolicitud_colaborador=False, comisionadosolicitud_chofer=False,
        )
        self.incorporacion.refresh_from_db()
        self.assertIsNone(self.incorporacion.incorporacion_texto_actuacion)

    def test_agregar_agente_directo_a_la_incorporacion_invalida_su_texto(self):
        self.ComisionadoSolicitud.objects.create(
            comisionadosolicitud_incorporacion_foreign=self.incorporacion, comisionadosolicitud_nombre=self.agente,
            comisionadosolicitud_colaborador=False, comisionadosolicitud_chofer=False,
        )
        self.incorporacion.refresh_from_db()
        self.assertIsNone(self.incorporacion.incorporacion_texto_actuacion)

    def test_cambiar_solicitud_no_toca_texto_propio_de_otra_incorporacion_inexistente(self):
        """Una Solicitud sin Incorporacion asociada no debe romper la invalidación."""
        self.solicitud.solicitud_texto_actuacion = {"parrafos": ["x"], "articulo_uno": "x", "articulo_dos": []}
        self.solicitud.save(update_fields=["solicitud_texto_actuacion"])
        self.solicitud.solicitud_actuacion_numero = 42
        self.solicitud.solicitud_texto_actuacion = None
        self.solicitud.save()  # no debe tirar excepción aunque no haya texto que invalidar
