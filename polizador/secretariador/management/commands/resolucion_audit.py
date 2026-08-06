from django.core.management.base import BaseCommand
from django.db.models import Max
from secretariador.models import InstrumentosLegalesResoluciones


class Command(BaseCommand):
    help = (
        "Verifica que la numeración de las resoluciones cargadas sea consecutiva "
        "para cada año, reportando los números faltantes (indican un error de carga)."
    )

    def handle(self, *args, **kwargs):
        # Antes de 2022 los datos son legacy y están parcialmente digitalizados
        # (pocos registros con numeración muy salteada), no cargas secuenciales
        # reales, así que auditarlos solo genera falsos positivos.
        # Se deberá modificar el valor si en algún momento se digitalizan el
        # resto de los datos.
        ANO_MINIMO = "2022"

        anos = (
            InstrumentosLegalesResoluciones.objects.filter(
                instrumentolegalresoluciones_ano__gte=ANO_MINIMO
            )
            .order_by("instrumentolegalresoluciones_ano")
            .values_list("instrumentolegalresoluciones_ano", flat=True)
            .distinct()
        )

        total_faltantes = 0
        for ano in anos:
            resoluciones_del_ano = InstrumentosLegalesResoluciones.objects.filter(
                instrumentolegalresoluciones_ano=ano
            )
            numero_maximo = resoluciones_del_ano.aggregate(
                Max("instrumentolegalresoluciones_numero")
            )["instrumentolegalresoluciones_numero__max"]
            existentes = set(
                resoluciones_del_ano.values_list("instrumentolegalresoluciones_numero", flat=True)
            )

            for numero in range(1, numero_maximo + 1):
                if numero not in existentes:
                    self.stdout.write(self.style.WARNING(f"La Resolución Nº{numero}/{ano} no existe"))
                    total_faltantes += 1

        if total_faltantes:
            self.stdout.write(self.style.ERROR(f"Total de resoluciones faltantes: {total_faltantes}"))
        else:
            self.stdout.write(self.style.SUCCESS("No se encontraron números faltantes."))
