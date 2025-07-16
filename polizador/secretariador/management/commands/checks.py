from django.core.management.base import BaseCommand, CommandError
from secretariador.models import *
from django.db.models import Sum, Q
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        Checks number continuity of the instrumentoslegalesresoluciones model.
        """
        ano_de_objeto = [2022, 2023, 2024, 2025]
        
        for ano in ano_de_objeto:
            numero_de_objeto = 1

            for _ in range(0, int(InstrumentosLegalesResoluciones.objects.filter(instrumentolegalresoluciones_ano=ano).first().instrumentolegalresoluciones_numero)):
                if not InstrumentosLegalesResoluciones.objects.filter(instrumentolegalresoluciones_ano=ano, instrumentolegalresoluciones_numero=str(numero_de_objeto).zfill(5)).exists():
                    print(f"La Resolución Nº{numero_de_objeto}/{ano} no existe")
                numero_de_objeto += 1