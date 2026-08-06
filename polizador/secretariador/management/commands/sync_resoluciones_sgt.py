"""
Sincroniza Resoluciones desde el SGT (Sistema Gestión de Trámites, app.chaco.gob.ar)
hacia InstrumentosLegalesResoluciones.

El SGT no tiene una API pública. Es una aplicación GeneXus ("Work With Plus") detrás de un
SSO propio del portal gobiernodigital.chaco.gob.ar. Este comando maneja un navegador real
(Playwright) porque el protocolo AJAX interno de GeneXus (tokens de estado por fila, IVs,
hashes de sesión) no está documentado, usa cifrado del lado del cliente y es impracticable
de reimplementar a mano; en cambio, se lo hace navegar la UI real tal como lo haría una
persona, y el navegador resuelve ese protocolo por nosotros.

Flujo (validado en vivo, no es una suposición leída de un HAR):
  1. Login por formulario en gobiernodigital.chaco.gob.ar (cookie de sesión Symfony).
  2. SSO hacia el SGT vía /aplicacion/22/launch (OAuth2 code flow interno, cookies propias
     de app.chaco.gob.ar: JSESSIONID + GX_SESSION_ID + GX_CLIENT_ID).
  3. Panel "Gestionar Proyectos de Instrumentos" (com.ecom.panelprotocolo), filtrado por
     Tipo = Resolución.
  4. Se exporta la grilla a Excel (botón nativo "BTNEXPORT" del panel): a diferencia de la
     grilla en pantalla (paginada de a 10), el export trae el listado COMPLETO, con una
     columna "Identificación" que ya viene en el mismo formato RES-YYYY-NNNN-10-N que
     InstrumentosLegalesResoluciones.instrumentolegalresoluciones_numero_sgt genera solo.
     Eso es lo que se usa para diffear contra lo que ya está cargado en Polizador.
  5. Por cada resolución que falte, se filtra el panel por número+año puntual y se hace click
     en "Ver Proyecto" de la fila resultante. Eso NO abre una ventana nueva: carga un iframe
     (com.ecom.verproyecto) dentro de la misma página (modal al estilo GeneXus). El PDF final
     queda referenciado ahí como /tramites/PublicTempStorage/<archivo>.pdf; se pide con el
     mismo contexto autenticado y se guarda en el modelo.

Nota sobre el navegador: el sitio tiene un WAF delante que bloquea específicamente al
Chromium/Chrome manejado por CDP (incluso el binario real de Chrome, incluso con
navigator.webdriver oculto) — probablemente por fingerprint de red (TLS/HTTP2), no por señales
de JS. Firefox vía Playwright NO tiene ese problema y fue lo que se usó para validar todo este
flujo. Por eso el comando lanza Firefox, no Chrome.

Requiere en el .env: SGT_USERNAME, SGT_PASSWORD (credenciales del usuario institucional).
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

from secretariador.models import InstrumentosLegalesResoluciones

DEBUG_DIR = Path("/tmp/sgt_debug")

GOBIERNO_DIGITAL_BASE = "https://gobiernodigital.chaco.gob.ar"
SGT_LAUNCH_URL = f"{GOBIERNO_DIGITAL_BASE}/aplicacion/22/launch"
SGT_TRAMITES_BASE = "https://app.chaco.gob.ar/tramites"
SGT_PANEL_URL = f"{SGT_TRAMITES_BASE}/servlet/com.ecom.panelprotocolo"

# Valor del <select id="vINSTRUMENTOPROYECTOINSTRUMENTOLEGALTIPO"> en el panel del SGT.
# Opciones vistas: 0=Todos, 1=DECRETO, 2=RESOLUCIÓN, 3=DISPOSICIÓN.
TIPO_RESOLUCION_SGT = "2"

# Solo se importan instrumentos en este estado; borradores/pendientes de firma se ignoran.
ESTADO_APROBADO = "instrumento aprobado"

IDENTIFICACION_RE = re.compile(r"RES-(\d{4})-(\d+)-10-(\d+)")
PDF_PATH_RE = re.compile(r"PublicTempStorage/[^\"'\s]*\.pdf", re.IGNORECASE)


class Command(BaseCommand):
    help = (
        "Descarga desde el SGT las Resoluciones que todavía no están cargadas en "
        "InstrumentosLegalesResoluciones y las guarda con autocarga=True."
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
            help="Solo informa qué resoluciones faltan, sin descargar ni guardar nada.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Descarga como máximo N resoluciones nuevas (útil para probar o para "
                 "catch-up incremental en corridas periódicas).",
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

        with sync_playwright() as p:
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
            self._abrir_panel_resoluciones(page)

            self.stdout.write(self.style.MIGRATE_LABEL("Exportando listado de Resoluciones..."))
            filas = self._listar_resoluciones(page)
            self.stdout.write(f"    {len(filas)} resoluciones aprobadas encontradas en el SGT.")

            existentes_por_ano = {}
            for numero, ano in InstrumentosLegalesResoluciones.objects.values_list(
                "instrumentolegalresoluciones_numero", "instrumentolegalresoluciones_ano"
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
                    self.stdout.write(
                        f"    {fila['identificacion']} - {fila['descripcion'][:80]}"
                    )
                browser.close()
                return

            if options["limit"]:
                faltantes = faltantes[: options["limit"]]

            for fila in faltantes:
                try:
                    self._descargar_y_guardar(page, fila)
                except Exception as e:
                    self.stdout.write(
                        f"{self.style.ERROR('Error procesando')} {fila['identificacion']}: {e}"
                    )
                    self._debug_dump(page, f"error_{fila['numero']}_{fila['ano']}")

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

    def _abrir_panel_resoluciones(self, page):
        page.goto(SGT_LAUNCH_URL)
        page.wait_for_load_state("networkidle")
        if "app.chaco.gob.ar" not in page.url:
            self._debug_dump(page, "03_sso_did_not_reach_sgt")
            raise CommandError(f"El SSO al SGT no llegó a app.chaco.gob.ar (url: {page.url}).")

        page.goto(SGT_PANEL_URL)
        page.wait_for_load_state("networkidle")
        try:
            page.select_option(
                "#vINSTRUMENTOPROYECTOINSTRUMENTOLEGALTIPO", TIPO_RESOLUCION_SGT, timeout=10000
            )
        except Exception:
            self._debug_dump(page, "04_tipo_filter_not_found")
            raise
        page.wait_for_load_state("networkidle")

    def _listar_resoluciones(self, page):
        import openpyxl

        try:
            with page.expect_download(timeout=20000) as download_info:
                page.click("#BTNEXPORT")
            download = download_info.value
            data = Path(download.path()).read_bytes()
        except Exception:
            self._debug_dump(page, "05_export_failed")
            raise

        # openpyxl decide el formato por la extensión del nombre de archivo; el path temporal
        # que da Playwright no tiene extensión, así que se le pasan los bytes directamente.
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True)
        ws = wb.active
        rows_iter = ws.iter_rows(values_only=True)

        header = None
        for row in rows_iter:
            if row and any(str(c).strip() == "Nro. Instr." for c in row if c is not None):
                header = [str(c).strip() if c is not None else "" for c in row]
                break
        if header is None:
            raise CommandError(
                "No encontré la fila de encabezados ('Nro. Instr.') en el Excel exportado."
            )

        idx_ident = header.index("Identificación")
        idx_tramite = header.index("Trámite")
        idx_desc = header.index("Descripción")
        idx_fecha = header.index("Fecha")
        idx_estado = header.index("Estado")

        filas = []
        omitidas_estado = 0
        for row in rows_iter:
            if not row or row[idx_ident] is None:
                continue
            identificacion = str(row[idx_ident]).strip()
            m = IDENTIFICACION_RE.match(identificacion)
            if not m:
                continue
            estado = str(row[idx_estado] or "").strip()
            if estado.lower() != ESTADO_APROBADO:
                omitidas_estado += 1
                continue
            tramite = str(row[idx_tramite] or "").strip()
            descripcion = str(row[idx_desc] or "").strip()
            filas.append({
                "identificacion": identificacion,
                "ano": m.group(1),
                "numero": m.group(2),
                "descripcion": f"{tramite}, {descripcion}" if tramite else descripcion,
                "fecha": row[idx_fecha],
            })

        if omitidas_estado:
            self.stdout.write(
                f"    ({omitidas_estado} filas omitidas por no estar en estado "
                f"'{ESTADO_APROBADO}')"
            )
        return filas

    def _filtrar_numero_ano(self, page, numero, ano):
        # Cada blur dispara un POST a com.ecom.panelprotocolo que devuelve la grilla ya
        # filtrada (confirmado inspeccionando la red en vivo). Antes se usaba una espera fija
        # (wait_for_timeout) tras el blur, pero cuando el SGT responde lento esa espera
        # quedaba corta: el código seguía de largo con la grilla todavía sin filtrar, y
        # get_by_title("Ver Proyecto").count() terminaba contando la página default de 10
        # filas en vez de la fila filtrada ("el filtro devolvió 10 filas (esperaba 1)").
        # Esperar la respuesta real del POST, en vez de un tiempo fijo, es inmune a eso.
        self._fill_y_esperar_filtro(page, "#vINSTRUMENTOLEGALNUMERO", numero)
        self._fill_y_esperar_filtro(page, "#vINSTRUMENTOLEGALANIO", ano)

    def _fill_y_esperar_filtro(self, page, selector, value):
        with page.expect_response(
            lambda r: "com.ecom.panelprotocolo" in r.url and r.request.method == "POST",
            timeout=15000,
        ):
            page.fill(selector, value)
            page.keyboard.press("Tab")
        # Pequeño margen para que el JS de GeneXus termine de pintar la grilla una vez
        # que ya tiene la respuesta (el fetch en sí ya se esperó arriba).
        page.wait_for_timeout(200)

    def _descargar_y_guardar(self, page, fila):
        # Filtra el panel a esta resolución puntual usando los inputs de búsqueda exacta
        # (más confiable que tratar de ubicar la fila correcta en una grilla paginada).
        self._filtrar_numero_ano(page, fila["numero"], fila["ano"])

        botones = page.get_by_title("Ver Proyecto")
        count = botones.count()
        if count != 1:
            self.stdout.write(
                f"{self.style.WARNING('Omitido')} {fila['identificacion']}: "
                f"el filtro devolvió {count} filas (esperaba 1)."
            )
            self._limpiar_filtro_numero_ano(page)
            return

        # "Ver Proyecto" no abre una ventana nueva: carga un iframe (modal) en la misma página.
        with page.expect_event("frameattached", timeout=15000) as frame_info:
            botones.first.click()
        frame = frame_info.value
        frame.wait_for_load_state("networkidle")

        m = PDF_PATH_RE.search(frame.content())
        if not m:
            self._cerrar_modal(page)
            raise CommandError("No encontré la referencia al PDF dentro de 'Ver Proyecto'.")
        pdf_url = f"{SGT_TRAMITES_BASE}/{m.group(0)}"

        resp = page.context.request.get(pdf_url)
        if resp.status != 200 or "pdf" not in resp.headers.get("content-type", ""):
            self._cerrar_modal(page)
            raise CommandError(f"Descarga de PDF falló (status {resp.status}): {pdf_url}")
        pdf_bytes = resp.body()

        self._cerrar_modal(page)
        self._limpiar_filtro_numero_ano(page)

        defaults = {
            "instrumentolegalresoluciones_tipo": "P",
            "instrumentolegalresoluciones_descripcion": (
                fila["descripcion"] or "Resolución importada desde el SGT"
            )[:600],
            "instrumentolegalresoluciones_autocarga": True,
        }
        fecha = fila["fecha"]
        if isinstance(fecha, datetime.datetime):
            fecha = fecha.date()
        if isinstance(fecha, datetime.date):
            defaults["instrumentolegalresoluciones_fecha_aprobacion"] = fecha

        instrumento, created = InstrumentosLegalesResoluciones.objects.get_or_create(
            instrumentolegalresoluciones_numero=int(fila["numero"]),
            instrumentolegalresoluciones_ano=fila["ano"],
            instrumentolegalresoluciones_acta="",
            defaults=defaults,
        )
        instrumento.instrumentolegalresoluciones.save(
            f"{fila['identificacion']}.pdf", ContentFile(pdf_bytes), save=True
        )

        estado = "creada" if created else "actualizada (ya existía, se reemplazó el archivo)"
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

    def _limpiar_filtro_numero_ano(self, page):
        self._filtrar_numero_ano(page, "0", "0")
