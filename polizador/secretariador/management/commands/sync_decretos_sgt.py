"""
Sincroniza Decretos que establecen períodos de licencia (anual/invierno) desde el SGT
(Sistema Gestión de Trámites, app.chaco.gob.ar) hacia InstrumentosLegalesDecretos.

Mismo mecanismo que sync_resoluciones_sgt.py (leer ese archivo para el detalle completo del
flujo SSO/panel/export/descarga): el SGT no tiene una API pública, es una aplicación GeneXus
("Work With Plus") detrás de un SSO propio de gobiernodigital.chaco.gob.ar, y se navega con un
navegador real (Playwright/Firefox, no Chromium por el WAF) tal como lo haría una persona.

Flujo:
  1. Login por formulario en gobiernodigital.chaco.gob.ar (cookie de sesión Symfony).
  2. SSO hacia el SGT vía /aplicacion/22/launch.
  3. Búsqueda de instrumentos (com.ecom.busquedainstrumentos), filtrado por Tipo = Decreto.
  4. Se exporta la grilla a Excel (botón "BTNEXPORT"): trae el listado COMPLETO de decretos
     protocolizados y publicados, no solo la página en pantalla. A diferencia del Excel de
     Resoluciones, este NO tiene columna "Estado" ni "Nro. Instr." — el título del propio
     reporte ("Listado de instrumentos legales protocolizados y publicados") ya implica que
     todo lo que aparece está aprobado, no hace falta filtrar por estado. Las columnas reales
     (confirmadas contra un export real) son: Instrumento, Identificación, Protoc., Descripción,
     Referencia, Publicación, Temáticas, Gestión, Trámite — bien distintas a las de Resoluciones.
  5. A diferencia de sync_resoluciones_sgt (que importa TODAS las resoluciones aprobadas), acá
     se filtra el listado exportado por columna para quedarse solo con los decretos que
     establecen un período de licencia anual ordinaria o de invierno — el resto del universo de
     decretos (en su mayoría escalas de viáticos) se ignora, ya que se sigue cargando
     manualmente como hasta ahora. El filtro (confirmado contra el panel real) es:
       - Licencia Anual Ordinaria: columna "Temáticas" ∈ {"LICENCIAS", "LICENCIAS - OTRO"} y
         columna "Referencia" contiene "determina".
       - Licencia Anual de Invierno: columna "Temáticas" = "LICENCIAS" y columna "Descripción"
         contiene "invierno".
  6. Por cada decreto faltante que matcheó el filtro, se busca por Identificación exacta usando
     el "Dynamic Filter" de la página (#vDYNAMICFILTERSSELECTOR1 + #vINSTRUMENTOLEGALCLAVE1) —
     esta página NO tiene los inputs fijos #vINSTRUMENTOLEGALNUMERO/#vINSTRUMENTOLEGALANIO que sí
     tiene el panel de Resoluciones (com.ecom.panelprotocolo); usarlos ahí causaba timeout. Se
     hace click en el botón de fila con title "ver Instrumento" (NO "Ver Proyecto", que es el de
     Resoluciones) y de ahí se extrae la referencia al PDF (PublicTempStorage/...) y se descarga
     con el mismo contexto autenticado.

Correr primero con --dry-run --headed y ajustar eso mirando el sitio real antes de confiar en el
resto del comando. El formato de "Identificación" (DEC-YYYY-NNNN-APP-CHACO), el filtro de
detección de licencia (columnas Temáticas/Descripción/Referencia) y el mecanismo de búsqueda por
Identificación (Dynamic Filter) ya fueron confirmados contra el sitio real, no son una suposición.
SIN VALIDAR EN VIVO todavía: si al hacer click en "ver Instrumento" se abre un iframe modal igual
que "Ver Proyecto" en Resoluciones (com.ecom.verproyecto) — correr con --headed --limit 1 para
confirmarlo antes de una corrida completa.

Requiere en el .env: SGT_USERNAME, SGT_PASSWORD (las mismas credenciales que sync_resoluciones_sgt).
Requiere el navegador de Playwright instalado una vez: `playwright install firefox`.
"""
import datetime
import io
import os
import re
from pathlib import Path

# Playwright deja el hilo principal con un event loop "activo" para su puente sync/async.
# Django, por seguridad, bloquea el ORM en cualquier hilo que parezca async (evita deadlocks
# en apps ASGI). Acá no hay tal riesgo: este comando es un script de una sola corrida, no un
# server. Es el workaround estándar para usar el ORM junto con la API sync de Playwright.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from secretariador.models import InstrumentosLegalesDecretos

DEBUG_DIR = Path("/tmp/sgt_debug_decretos")

GOBIERNO_DIGITAL_BASE = "https://gobiernodigital.chaco.gob.ar"
SGT_LAUNCH_URL = f"{GOBIERNO_DIGITAL_BASE}/aplicacion/22/launch"
SGT_TRAMITES_BASE = "https://app.chaco.gob.ar/tramites"
SGT_PANEL_URL = f"{SGT_TRAMITES_BASE}/servlet/com.ecom.busquedainstrumentos"

# Valor del <select id="vINSTRUMENTOPROYECTOINSTRUMENTOLEGALTIPO"> en el panel del SGT.
# Opciones vistas (confirmadas para Resolución, inferidas para Decreto): 0=Todos, 1=DECRETO,
# 2=RESOLUCIÓN, 3=DISPOSICIÓN. SIN VALIDAR EN VIVO para Decreto específicamente.
TIPO_DECRETO_SGT = "1"

# Formato confirmado contra el panel real: "DEC-2025-1839-APP-CHACO" ->
# tipo(DEC)-año-numero-APP-CHACO.
IDENTIFICACION_RE = re.compile(r"DEC-(\d{4})-(\d+)-APP-CHACO")
PDF_PATH_RE = re.compile(r"PublicTempStorage/[^\"'\s]*\.pdf", re.IGNORECASE)

# Filtro estructurado por columna del Excel exportado, confirmado contra el panel real de
# búsqueda de instrumentos (com.ecom.busquedainstrumentos). Los dos casos se chequean de forma
# independiente: un decreto puede matchear ambos (y en ese caso ambos flags quedan en True).
#   - Licencia Anual Ordinaria: Temáticas ∈ TEMATICAS_LICENCIA_ANUAL y "Referencia" contiene
#     REFERENCIA_ANUAL_KEYWORD.
#   - Licencia Anual de Invierno: Temáticas == TEMATICA_LICENCIA_INVIERNO y "Descripción"
#     contiene DESCRIPCION_INVIERNO_KEYWORD.
TEMATICAS_LICENCIA_ANUAL = ("LICENCIAS", "LICENCIAS - OTRO")
REFERENCIA_ANUAL_KEYWORD = "determina"
TEMATICA_LICENCIA_INVIERNO = "LICENCIAS"
DESCRIPCION_INVIERNO_KEYWORD = "invierno"


class Command(BaseCommand):
    help = (
        "Descarga desde el SGT los Decretos que establecen un período de licencia anual "
        "ordinaria o de invierno y aún no están cargados en InstrumentosLegalesDecretos, "
        "marcando los flags correspondientes."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--headed",
            action="store_true",
            help="Corre el navegador con interfaz visible, útil para depurar selectores.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Solo informa qué decretos matchean y faltan, sin descargar ni guardar nada.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Descarga como máximo N decretos nuevos (útil para probar o para catch-up "
                 "incremental en corridas periódicas).",
        )
        parser.add_argument(
            "--solo-excel",
            action="store_true",
            help="Solo exporta el listado a un Excel en MEDIA_ROOT/sgt_exports/ y termina, "
                 "sin parsear ni descargar ningún decreto individual.",
        )
        parser.add_argument(
            "--forzar-descarga",
            action="store_true",
            help="Ignora cualquier Excel cacheado en MEDIA_ROOT/sgt_exports/ y fuerza una "
                 "exportación nueva desde el SGT (por defecto se reusa el más reciente para "
                 "no generar carga innecesaria contra el sitio).",
        )

    def handle(self, *args, **options):
        if not settings.SGT_USERNAME or not settings.SGT_PASSWORD:
            raise CommandError(
                "Faltan SGT_USERNAME / SGT_PASSWORD en el .env "
                "(credenciales del usuario institucional en gobiernodigital.chaco.gob.ar)."
            )

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise CommandError(
                "Falta playwright. Instalá con `pip install playwright` y despues "
                "`playwright install firefox`."
            )

        data = None
        if not options["forzar_descarga"] and not options["solo_excel"]:
            cache_path = self._buscar_excel_cacheado("decretos")
            if cache_path:
                self.stdout.write(
                    f"{self.style.MIGRATE_LABEL('Usando Excel cacheado:')} {cache_path} "
                    "(pasá --forzar-descarga para bajar un listado nuevo del SGT)"
                )
                data = cache_path.read_bytes()

        with sync_playwright() as p:
            browser = None
            page = None

            def _asegurar_sesion():
                nonlocal browser, page
                if browser is not None:
                    return page
                try:
                    browser = p.firefox.launch(headless=not options["headed"])
                except Exception as e:
                    raise CommandError(
                        f"No pude lanzar Firefox: {e}\n"
                        "¿Está instalado? Corré `playwright install firefox`."
                    )
                context = browser.new_context(
                    accept_downloads=True,
                    locale="es-AR",
                    timezone_id="America/Argentina/Buenos_Aires",
                    viewport={"width": 1920, "height": 1080},
                )
                page = context.new_page()
                self.stdout.write(self.style.MIGRATE_LABEL("Iniciando sesión en gobiernodigital..."))
                self._login(page)
                self.stdout.write(self.style.MIGRATE_LABEL("Abriendo SGT..."))
                self._abrir_panel_decretos(page)
                return page

            if options["solo_excel"]:
                page = _asegurar_sesion()
                self.stdout.write(self.style.MIGRATE_LABEL("Exportando listado de Decretos..."))
                data = self._exportar_excel(page)
                destino = self._guardar_excel_media(data, "decretos")
                self.stdout.write(self.style.SUCCESS(f"Excel guardado en {destino}"))
                browser.close()
                return

            if data is None:
                page = _asegurar_sesion()
                self.stdout.write(self.style.MIGRATE_LABEL("Exportando listado de Decretos..."))
                data = self._exportar_excel(page)
                self._guardar_excel_media(data, "decretos")

            filas = self._listar_decretos(data)
            self.stdout.write(
                f"    {len(filas)} decretos matchean el filtro de licencia."
            )

            existentes_por_ano = {}
            for numero, ano in InstrumentosLegalesDecretos.objects.values_list(
                "instrumentolegaldecretos_numero", "instrumentolegaldecretos_ano"
            ):
                existentes_por_ano.setdefault(str(ano), set()).add(numero)

            def _ya_existe(fila):
                return int(fila["numero"]) in existentes_por_ano.get(fila["ano"], set())

            faltantes = [fila for fila in filas if not _ya_existe(fila)]
            self.stdout.write(
                f"{self.style.MIGRATE_LABEL('Faltantes en Polizador:')} {len(faltantes)}"
            )

            if options["dry_run"]:
                for fila in faltantes:
                    tipo_str = ", ".join(
                        s for s in (
                            "anual" if fila["establece_licencia_anual"] else None,
                            "invierno" if fila["establece_licencia_invierno"] else None,
                        ) if s
                    )
                    self.stdout.write(
                        f"    {fila['identificacion']} [{tipo_str}] - {fila['descripcion'][:80]}"
                    )
                if browser:
                    browser.close()
                return

            if options["limit"]:
                faltantes = faltantes[: options["limit"]]

            if faltantes:
                page = _asegurar_sesion()
                for fila in faltantes:
                    try:
                        self._descargar_y_guardar(page, fila)
                    except Exception as e:
                        self.stdout.write(
                            f"{self.style.ERROR('Error procesando')} {fila['identificacion']}: {e}"
                        )
                        self._debug_dump(page, f"error_{fila['numero']}_{fila['ano']}")

            if browser:
                browser.close()

    # -- Diagnóstico -----------------------------------------------------------

    def _debug_dump(self, page, name):
        """Guarda screenshot + HTML de la página actual para diagnosticar selectores rotos."""
        DEBUG_DIR.mkdir(parents=True, exist_ok=True)
        png_path = DEBUG_DIR / f"{name}.png"
        html_path = DEBUG_DIR / f"{name}.html"
        try:
            page.screenshot(path=str(png_path), full_page=True)
            html_path.write_text(page.content())
            self.stdout.write(
                f"{self.style.WARNING('Diagnóstico guardado:')} {png_path} / {html_path} "
                f"(url actual: {page.url})"
            )
        except Exception as e:
            self.stdout.write(f"{self.style.WARNING('No pude guardar el diagnóstico:')} {e}")

    # -- Pasos del navegador -----------------------------------------------------

    def _login(self, page):
        page.goto(f"{GOBIERNO_DIGITAL_BASE}/login")
        page.wait_for_load_state("domcontentloaded")
        try:
            page.fill('input[name="_username"]', settings.SGT_USERNAME, timeout=10000)
            page.fill('input[name="_password"]', settings.SGT_PASSWORD, timeout=10000)
        except Exception:
            self._debug_dump(page, "01_login_form_not_found")
            raise
        with page.expect_navigation():
            page.click('button[type="submit"], input[type="submit"]')
        if "/login" in page.url:
            self._debug_dump(page, "02_login_did_not_redirect")
            raise CommandError(
                "El login no redirigió fuera de /login. Revisar credenciales."
            )

    def _abrir_panel_decretos(self, page):
        page.goto(SGT_LAUNCH_URL)
        page.wait_for_load_state("networkidle")
        if "app.chaco.gob.ar" not in page.url:
            self._debug_dump(page, "03_sso_did_not_reach_sgt")
            raise CommandError(f"El SSO al SGT no llegó a app.chaco.gob.ar (url: {page.url}).")

        page.goto(SGT_PANEL_URL)
        page.wait_for_load_state("networkidle")
        try:
            page.select_option(
                "#vINSTRUMENTOPROYECTOINSTRUMENTOLEGALTIPO", TIPO_DECRETO_SGT, timeout=10000
            )
        except Exception:
            self._debug_dump(page, "04_tipo_filter_not_found")
            raise
        page.wait_for_load_state("networkidle")

    def _exportar_excel(self, page):
        """Dispara la exportación nativa del panel (botón "BTNEXPORT") y devuelve los bytes
        crudos del Excel descargado, sin parsear nada."""
        try:
            with page.expect_download(timeout=20000) as download_info:
                page.click("#BTNEXPORT")
            download = download_info.value
            return Path(download.path()).read_bytes()
        except Exception:
            self._debug_dump(page, "05_export_failed")
            raise

    def _guardar_excel_media(self, data, prefix):
        """Guarda el Excel exportado en MEDIA_ROOT/sgt_exports/, para reuso en corridas futuras
        (ver _buscar_excel_cacheado) y para --solo-excel."""
        directorio = Path(settings.MEDIA_ROOT) / "sgt_exports"
        directorio.mkdir(parents=True, exist_ok=True)
        nombre = f"{prefix}_{datetime.datetime.now():%Y%m%d_%H%M%S}.xlsx"
        destino = directorio / nombre
        destino.write_bytes(data)
        return destino

    def _buscar_excel_cacheado(self, prefix):
        """Devuelve el Excel más reciente ya exportado en MEDIA_ROOT/sgt_exports/ para este
        prefijo (resoluciones/decretos), o None si no hay ninguno. El nombre de archivo incluye
        un timestamp ordenable (YYYYMMDD_HHMMSS), así que ordenar por nombre alcanza."""
        directorio = Path(settings.MEDIA_ROOT) / "sgt_exports"
        if not directorio.is_dir():
            return None
        candidatos = sorted(directorio.glob(f"{prefix}_*.xlsx"))
        return candidatos[-1] if candidatos else None

    def _listar_decretos(self, data):
        import openpyxl

        # openpyxl decide el formato por la extensión del nombre de archivo; el path temporal
        # que da Playwright no tiene extensión, así que se le pasan los bytes directamente.
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True)
        ws = wb.active
        rows_iter = ws.iter_rows(values_only=True)

        # A diferencia del export de Resoluciones, este no tiene "Nro. Instr." como ancla de la
        # fila de encabezados (ni columna "Estado": el reporte ya viene filtrado a instrumentos
        # protocolizados y publicados). Se ancla en "Identificación", que sí está presente.
        header = None
        for row in rows_iter:
            if row and any(str(c).strip() == "Identificación" for c in row if c is not None):
                header = [str(c).strip() if c is not None else "" for c in row]
                break
        if header is None:
            raise CommandError(
                "No encontré la fila de encabezados ('Identificación') en el Excel exportado."
            )

        # Columnas reales del export de Decretos (com.ecom.busquedainstrumentos), confirmadas
        # contra un archivo real: Instrumento, Identificación, Protoc., Descripción, Referencia,
        # Publicación, Temáticas, Gestión, Trámite. "Trámite" acá es el número de expediente
        # (ej. "E 28-2026-12695-Ae"), no texto descriptivo como en Resoluciones — se antepone a
        # la descripción igual para trazabilidad, pero "Referencia" es la que se usa para el
        # filtro de Licencia Anual Ordinaria (columna Referencia contiene "determina").
        idx_instrumento = header.index("Instrumento")
        idx_ident = header.index("Identificación")
        idx_protoc = header.index("Protoc.")
        idx_desc = header.index("Descripción")
        idx_referencia = header.index("Referencia")
        idx_tematicas = header.index("Temáticas")
        idx_tramite = header.index("Trámite")

        filas = []
        total_decretos = 0
        for row in rows_iter:
            if not row or row[idx_ident] is None:
                continue
            instrumento = str(row[idx_instrumento] or "").strip()
            if instrumento.upper() != "DECRETO":
                continue
            identificacion = str(row[idx_ident]).strip()
            m = IDENTIFICACION_RE.match(identificacion)
            if not m:
                continue
            total_decretos += 1
            descripcion = str(row[idx_desc] or "").strip()
            referencia = str(row[idx_referencia] or "").strip()
            tematicas = str(row[idx_tematicas] or "").strip()
            tramite = str(row[idx_tramite] or "").strip()

            establece_anual = (
                tematicas in TEMATICAS_LICENCIA_ANUAL
                and REFERENCIA_ANUAL_KEYWORD in referencia.lower()
            )
            establece_invierno = (
                tematicas == TEMATICA_LICENCIA_INVIERNO
                and DESCRIPCION_INVIERNO_KEYWORD in descripcion.lower()
            )
            if not (establece_anual or establece_invierno):
                continue
            filas.append({
                "identificacion": identificacion,
                "ano": m.group(1),
                "numero": m.group(2),
                "descripcion": f"{tramite}, {descripcion}" if tramite else descripcion,
                # "Protoc." (fecha de protocolización) es el equivalente más cercano a la fecha
                # de aprobación del decreto; "Publicación" es posterior (cuando se publicó).
                "fecha": row[idx_protoc],
                "establece_licencia_anual": establece_anual,
                "establece_licencia_invierno": establece_invierno,
            })

        self.stdout.write(
            f"    {total_decretos} decretos encontrados en el SGT, "
            f"{len(filas)} matchean el filtro de licencia (Temáticas/Descripción/Referencia)."
        )
        return filas

    def _filtrar_identificacion(self, page, identificacion):
        # A diferencia del panel de Resoluciones (com.ecom.panelprotocolo), esta página
        # (com.ecom.busquedainstrumentos) NO tiene inputs fijos #vINSTRUMENTOLEGALNUMERO /
        # #vINSTRUMENTOLEGALANIO — confirmado con un --headed real: rellenarlos hacía que
        # page.fill() esperara por un selector que no existe y terminara en timeout. El
        # filtro real acá es un "Dynamic Filter" genérico: un <select> de columna
        # (#vDYNAMICFILTERSSELECTOR1) + un input de valor cuyo id cambia según la columna
        # elegida. Con "Identificación" seleccionada (option value="INSTRUMENTOLEGALCLAVE",
        # que además es la que viene seleccionada por default), el input de valor es
        # #vINSTRUMENTOLEGALCLAVE1. Como la Identificación es la clave de negocio única del
        # decreto, alcanza con este único filtro (no hace falta combinar número+año).
        page.select_option("#vDYNAMICFILTERSSELECTOR1", "INSTRUMENTOLEGALCLAVE", timeout=10000)
        # El cambio de columna solo alterna visibilidad de inputs ya presentes en el DOM via
        # JS del lado del cliente (no dispara un POST): un margen chico alcanza para que el
        # input de "Identificación" quede visible antes de completarlo.
        page.wait_for_timeout(200)
        self._fill_y_esperar_filtro(page, "#vINSTRUMENTOLEGALCLAVE1", identificacion)

    def _fill_y_esperar_filtro(self, page, selector, value):
        with page.expect_response(
            lambda r: "com.ecom.busquedainstrumentos" in r.url and r.request.method == "POST",
            timeout=15000,
        ):
            page.fill(selector, value)
            page.keyboard.press("Tab")
        # Pequeño margen para que el JS de GeneXus termine de pintar la grilla una vez
        # que ya tiene la respuesta (el fetch en sí ya se esperó arriba).
        page.wait_for_timeout(200)

    def _descargar_y_guardar(self, page, fila):
        # Filtra la búsqueda a este decreto puntual por Identificación exacta (más confiable
        # que tratar de ubicar la fila correcta en una grilla paginada).
        self._filtrar_identificacion(page, fila["identificacion"])

        # El título del botón de acción por fila en esta página es "ver Instrumento" (así, en
        # minúscula), NO "Ver Proyecto" como en el panel de Resoluciones — confirmado contra
        # el HTML real de la grilla.
        botones = page.get_by_title("ver Instrumento")

        # _fill_y_esperar_filtro ya esperó la respuesta del POST que dispara el filtro, pero
        # esta grilla (Dynamic Filter) tarda un rato extra en repintarse después de esa
        # respuesta: si se chequea count() apenas se resuelve el POST, todavía se ve la
        # página sin filtrar (10 filas, la paginación default), no el resultado filtrado. Un
        # assert auto-reintentable (en vez de un timeout fijo) espera hasta que la grilla
        # realmente refleje el filtro, o hasta 10s si nunca llega a exactamente 1 fila.
        from playwright.sync_api import expect as pw_expect
        try:
            pw_expect(botones).to_have_count(1, timeout=10000)
        except AssertionError:
            count = botones.count()
            self.stdout.write(
                f"{self.style.WARNING('Omitido')} {fila['identificacion']}: "
                f"el filtro devolvió {count} filas (esperaba 1)."
            )
            self._limpiar_filtro_identificacion(page)
            return

        # SIN VALIDAR EN VIVO a partir de acá: no se confirmó todavía si "ver Instrumento"
        # abre un iframe modal igual que "Ver Proyecto" en Resoluciones (com.ecom.verproyecto)
        # o se comporta distinto en esta página. Correr con --headed --limit 1 y ajustar este
        # bloque si el modal/iframe no aparece tal cual.
        with page.expect_event("frameattached", timeout=15000) as frame_info:
            botones.first.click()
        frame = frame_info.value
        frame.wait_for_load_state("networkidle")

        m = PDF_PATH_RE.search(frame.content())
        if not m:
            self._cerrar_modal(page)
            raise CommandError("No encontré la referencia al PDF dentro de 'ver Instrumento'.")
        pdf_url = f"{SGT_TRAMITES_BASE}/{m.group(0)}"

        resp = page.context.request.get(pdf_url)
        if resp.status != 200 or "pdf" not in resp.headers.get("content-type", ""):
            self._cerrar_modal(page)
            raise CommandError(f"Descarga de PDF falló (status {resp.status}): {pdf_url}")
        pdf_bytes = resp.body()

        self._cerrar_modal(page)
        self._limpiar_filtro_identificacion(page)

        defaults = {
            "instrumentolegaldecretos_descripcion": (
                fila["descripcion"] or "Decreto importado desde el SGT"
            )[:600],
            "instrumentolegaldecretos_establece_licencia_anual": fila["establece_licencia_anual"],
            "instrumentolegaldecretos_establece_licencia_invierno": fila["establece_licencia_invierno"],
        }
        fecha = fila["fecha"]
        if isinstance(fecha, datetime.datetime):
            fecha = fecha.date()
        if isinstance(fecha, datetime.date):
            defaults["instrumentolegaldecretos_fecha_aprobacion"] = fecha

        instrumento, created = InstrumentosLegalesDecretos.objects.get_or_create(
            instrumentolegaldecretos_numero=int(fila["numero"]),
            instrumentolegaldecretos_ano=fila["ano"],
            instrumentolegaldecretos_tipo="P",
            defaults=defaults,
        )
        instrumento.instrumentolegaldecretos.save(
            f"{fila['identificacion']}.pdf", ContentFile(pdf_bytes), save=True
        )

        estado = "creado" if created else "actualizado (ya existía, se reemplazó el archivo)"
        self.stdout.write(
            f"{self.style.SUCCESS('OK')} {fila['identificacion']} {estado} "
            f"({len(pdf_bytes)} bytes)."
        )

    def _cerrar_modal(self, page):
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
        except Exception:
            pass

    def _limpiar_filtro_identificacion(self, page):
        self._filtrar_identificacion(page, "")
