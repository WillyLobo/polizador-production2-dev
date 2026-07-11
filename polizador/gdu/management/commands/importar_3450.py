import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from gdu.models import Adjudicatario3450

PAGE_SIZE = 5000
MAXIMO = 70000


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
        actualizados = 0
        for r in registros:
            fecha = r.get("AdjuGISResFecha")
            if fecha == "0000-00-00T00:00:00":
                fecha = None
            Adjudicatario3450.objects.update_or_create(
                adjugisnroadju=r["AdjuGISNroAdju"],
                defaults={
                    "adjugisescritura": r.get("AdjuGISEscritura"),
                    "adjugisresacta": r.get("AdjuGISResActa"),
                    "adjugisresfecha": fecha,
                    "adjugisresnro": r.get("AdjuGISResNro"),
                    "adjugisapeynom": r.get("AdjuGISapeynom"),
                    "adjugisdireccion": r.get("AdjuGISdireccion"),
                    "adjugisdni": r.get("AdjuGISdni"),
                    "adjugismatricula": r.get("AdjuGISmatricula"),
                    "adjugismotivo": r.get("AdjuGISmotivo"),
                    "adjugissituacion": r.get("AdjuGISsituacion"),
                },
            )
            actualizados += 1
        return actualizados
