"""
Calcula y cachea el CRC-32 (IEEE, el mismo algoritmo del formato ZIP) de las
resoluciones que ya tienen un archivo cargado pero fueron subidas antes de que
existiera secretariador/signals.py::calcular_crc32_resolucion.

Es una corrida de una sola vez: una vez que todas las resoluciones existentes
tienen su CRC-32 cacheado, el signal se encarga de las nuevas subidas y este
comando no debería tener nada más para hacer (queda para correr manualmente
si en algún momento aparecen filas sin este dato, por ejemplo tras una carga
masiva que haya evitado el signal).
"""
import zlib

from django.core.management.base import BaseCommand

from secretariador.models import InstrumentosLegalesResoluciones


class Command(BaseCommand):
    help = "Calcula el CRC-32 de las resoluciones con archivo que todavía no lo tienen cacheado."

    def handle(self, *args, **options):
        pendientes = InstrumentosLegalesResoluciones.objects.exclude(
            instrumentolegalresoluciones=""
        ).filter(instrumentolegalresoluciones_crc32__isnull=True)

        total = pendientes.count()
        if not total:
            self.stdout.write("No hay resoluciones pendientes de calcular su CRC-32.")
            return

        self.stdout.write(f"Calculando CRC-32 para {total} resoluciones...")
        for indice, resolucion in enumerate(pendientes.iterator(), start=1):
            crc = 0
            with resolucion.instrumentolegalresoluciones.open("rb") as archivo:
                for chunk in archivo.chunks():
                    crc = zlib.crc32(chunk, crc)

            resolucion.instrumentolegalresoluciones_crc32 = crc
            resolucion.save(update_fields=["instrumentolegalresoluciones_crc32"])
            self.stdout.write(f"  [{indice}/{total}] {resolucion} -> {crc}")

        self.stdout.write(self.style.SUCCESS("Listo."))
