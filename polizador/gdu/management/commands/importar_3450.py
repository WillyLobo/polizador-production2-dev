import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from gdu.etl.importador import SI_NO
from gdu.models import Adjudicatario3450

PAGE_SIZE = 5000
# corte de seguridad: se lee de a páginas hasta la primera vacía (el piloto paraba fijo en
# 70.000 y el número máximo ya pasa de 81.000)
MAXIMO = 1_000_000
CAMPOS = [
    "apellido_nombre", "dni", "direccion", "escritura", "matricula", "res_nro", "res_fecha", "res_acta",
    "motivo", "situacion",
]


class Command(BaseCommand):
    """
    Equivalente a controllers/3450-import.js::s3450Import (antes disparado por
    node-cron los domingos y jueves a las 3am: '0 3 * * 0,4'). Programar como
    tarea de systemd timer / cron del sistema apuntando a:
        python manage.py importar_3450
    """
    help = "Importa/actualiza masivamente adjudicatarios desde la API 3450 del Gobierno del Chaco"

    def handle(self, *args, **options):
        token = self._login()

        for pagina in range(MAXIMO // PAGE_SIZE):
            desde = pagina * PAGE_SIZE + 1
            hasta = pagina * PAGE_SIZE + PAGE_SIZE

            registros, token = self._consultar(desde, hasta, token)
            if not registros:
                self.stdout.write(self.style.WARNING(f"Sin datos desde {desde}, se corta la importación"))
                break

            actualizados = self._upsert(registros)
            self.stdout.write(f"{desde}-{hasta}: {actualizados} registros actualizados")

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
            token = self._login()
            return self._consultar(desde, hasta, token, reintentar=False)
        resp.raise_for_status()
        return resp.json().get("SDTDatosAdjuGISCol", []), token

    def _upsert(self, registros):
        """Alta o actualización en bloque. estado_regularizacion no viene de la API: se conserva."""
        filas = []
        for r in registros:
            fecha = r.get("AdjuGISResFecha")
            if fecha == "0000-00-00T00:00:00":
                fecha = None
            filas.append(Adjudicatario3450(
                nro_adjudicatario=r["AdjuGISNroAdju"],
                apellido_nombre=(r.get("AdjuGISapeynom") or "").strip(),
                dni=r.get("AdjuGISdni") or None,
                direccion=(r.get("AdjuGISdireccion") or "").strip(),
                escritura=SI_NO.get((r.get("AdjuGISEscritura") or "").strip().upper()),
                matricula=(r.get("AdjuGISmatricula") or "").strip(),
                res_nro=r.get("AdjuGISResNro") or None,
                res_fecha=fecha or None,
                res_acta=r.get("AdjuGISResActa") or "",
                motivo=r.get("AdjuGISmotivo") or "",
                situacion=(r.get("AdjuGISsituacion") or "").strip(),
            ))
        Adjudicatario3450.objects.bulk_create(
            filas, update_conflicts=True, unique_fields=["nro_adjudicatario"], update_fields=[*CAMPOS, "actualizado_en"],
        )
        return len(filas)
