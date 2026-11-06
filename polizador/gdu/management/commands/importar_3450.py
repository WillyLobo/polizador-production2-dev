import logging
from datetime import date

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError

from gdu.etl.importador import SI_NO
from gdu.models import Adjudicatario3450

logger = logging.getLogger(__name__)

PAGE_SIZE = 5000
# corte de seguridad: se lee de a páginas hasta la primera vacía (el piloto paraba fijo en
# 70.000 y el número máximo ya pasa de 81.000)
MAXIMO = 1_000_000
CAMPOS = [
    "apellido_nombre", "dni", "direccion", "escritura", "matricula", "res_nro", "res_fecha", "res_acta",
    "motivo", "situacion",
]


def _fecha(valor):
    """La API manda fechas como datetime ("2015-08-13T00:00:00") y "0000-00-00T00:00:00" para vacío."""
    if not valor or valor.startswith("0000-00-00"):
        return None
    return date.fromisoformat(valor[:10])


def _entero(valor):
    return int(valor) if valor not in (None, "") else None


class Command(BaseCommand):
    """
    Equivalente a controllers/3450-import.js::s3450Import (antes disparado por
    node-cron los domingos y jueves a las 3am: '0 3 * * 0,4'). Programar como
    tarea de systemd timer / cron del sistema apuntando a:
        python manage.py importar_3450

    Loguea a gdu.management.commands.importar_3450 (consola + logs/django.log vía el
    logger root). Un registro que no se puede convertir se descarta con WARNING y una
    página que falla al guardarse se loguea con ERROR; en ambos casos se sigue con el
    resto, y si alguna página falló el comando termina con error para que cron lo note.
    """
    help = "Importa/actualiza masivamente adjudicatarios desde la API 3450 del Gobierno del Chaco"

    def handle(self, *args, **options):
        logger.info("Inicio de la importación 3450")
        try:
            token = self._login()
        except requests.RequestException as e:
            logger.exception("No se pudo obtener el token de la API 3450")
            raise CommandError(f"Login en la API 3450 falló: {e}") from e

        total = descartados = 0
        paginas_fallidas = []
        for pagina in range(MAXIMO // PAGE_SIZE):
            desde = pagina * PAGE_SIZE + 1
            hasta = pagina * PAGE_SIZE + PAGE_SIZE

            try:
                registros, token = self._consultar(desde, hasta, token)
            except (requests.RequestException, ValueError) as e:
                logger.exception("Falló la consulta a la API 3450 para %s-%s", desde, hasta)
                raise CommandError(f"Consulta {desde}-{hasta} a la API 3450 falló: {e}") from e
            if not registros:
                logger.info("Sin datos desde %s, se corta la importación", desde)
                break

            try:
                guardados, salteados = self._upsert(registros)
            except DatabaseError:
                logger.exception("No se pudo guardar la página %s-%s (%s registros)", desde, hasta, len(registros))
                paginas_fallidas.append(f"{desde}-{hasta}")
                continue
            total += guardados
            descartados += salteados
            logger.info("%s-%s: %s guardados, %s descartados", desde, hasta, guardados, salteados)

        logger.info(
            "Fin de la importación 3450: %s guardados, %s descartados, %s páginas fallidas",
            total, descartados, len(paginas_fallidas),
        )
        if paginas_fallidas:
            raise CommandError(f"Páginas que no se pudieron guardar: {', '.join(paginas_fallidas)}")

    def _login(self):
        resp = requests.post(
            f"{settings.GDU_3450_IMPORT_API_BASE_URL}/oauth/access_token",
            data={
                "username": settings.GDU_3450_IMPORT_API_USERNAME,
                "password": settings.GDU_3450_IMPORT_API_PASSWORD,
                "client_id": settings.GDU_3450_IMPORT_API_CLIENT_ID,
                "grant_type": "password",
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

    def _consultar(self, desde, hasta, token, reintentar=True):
        resp = requests.post(
            f"{settings.GDU_3450_IMPORT_API_BASE_URL}/rest/wsIpduvAdjuGISCol",
            json={"desde": desde, "hasta": hasta},
            headers={"Authorization": token},
            timeout=60,
        )
        if resp.status_code == 401 and reintentar:
            logger.info("Token vencido, se vuelve a loguear")
            token = self._login()
            return self._consultar(desde, hasta, token, reintentar=False)
        resp.raise_for_status()
        return resp.json().get("SDTDatosAdjuGISCol", []), token

    def _fila(self, r):
        return Adjudicatario3450(
            nro_adjudicatario=int(r["AdjuGISNroAdju"]),
            apellido_nombre=(r.get("AdjuGISapeynom") or "").strip(),
            dni=_entero(r.get("AdjuGISdni")) or None,
            direccion=(r.get("AdjuGISdireccion") or "").strip(),
            escritura=SI_NO.get((r.get("AdjuGISEscritura") or "").strip().upper()),
            matricula=(r.get("AdjuGISmatricula") or "").strip(),
            res_nro=_entero(r.get("AdjuGISResNro")) or None,
            res_fecha=_fecha(r.get("AdjuGISResFecha")),
            res_acta=r.get("AdjuGISResActa") or "",
            motivo=r.get("AdjuGISmotivo") or "",
            situacion=(r.get("AdjuGISsituacion") or "").strip(),
        )

    def _upsert(self, registros):
        """Alta o actualización en bloque. estado_regularizacion no viene de la API: se conserva.

        Devuelve (guardados, descartados)."""
        # por número de adjudicatario: si la API repite uno en la misma página, gana el último
        # (Postgres rechaza un ON CONFLICT DO UPDATE que toque dos veces la misma fila)
        filas = {}
        descartados = 0
        for r in registros:
            try:
                fila = self._fila(r)
            except (KeyError, TypeError, ValueError) as e:
                descartados += 1
                logger.warning("Registro 3450 descartado (%s: %s): %r", type(e).__name__, e, r)
                continue
            filas[fila.nro_adjudicatario] = fila
        Adjudicatario3450.objects.bulk_create(
            filas.values(), update_conflicts=True, unique_fields=["nro_adjudicatario"], update_fields=[*CAMPOS, "actualizado_en"],
        )
        return len(filas), descartados
