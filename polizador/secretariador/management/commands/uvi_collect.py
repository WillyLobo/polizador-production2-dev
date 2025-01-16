from django.core.management.base import BaseCommand, CommandError
import requests
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from carga.models import Uvi

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        idvariable=32
        last_object = Uvi.objects.last()
        last_object_date = last_object.uvi_fecha
        counter = 0
        fecha_desde = last_object_date+timedelta(days=1)
        fecha_hasta = fecha_desde+timedelta(days=31)


        
        r = requests.get(f"https://api.bcra.gob.ar/estadisticas/v2.0/datosvariable/{idvariable}/{fecha_desde}/{fecha_hasta}", verify=False)
        r = dict(r.json())
        # Get last date of Uvi model to fill the last id and complete the sequence.
        for value in r["results"]:
            uvi_fecha = value["fecha"]
            uvi_valor = value["valor"]
            print(uvi_fecha, uvi_valor)
            try:
                uvi = Uvi.objects.get(uvi_fecha=uvi_fecha)
                if uvi_fecha == uvi.uvi_fecha and uvi_valor == uvi.uvi_valor:
                    print(f"{uvi} already exists.")
            except ObjectDoesNotExist:
                print(f"No record found... inserting new one.")
                uvi = Uvi(
                    id=int(last_object.id) + counter,
                    uvi_fecha=uvi_fecha,
                    uvi_valor=uvi_valor
                    )
                uvi.save()
                counter += 1

"""
{
  "status": 200,
  "results": [
    {
      "idVariable": 1,
      "cdSerie": 246,
      "descripcion": "Reservas Internacionales del BCRA (en millones de dólares - cifras provisorias sujetas a cambio de valuación)",
      "fecha": "2024-09-18",
      "valor": 27011
    },
    {
      "idVariable": 4,
      "cdSerie": 7927,
      "descripcion": "Tipo de Cambio Minorista ($ por USD) Comunicación B 9791 - Promedio vendedor",
      "fecha": "2024-09-20",
      "valor": 1000.01
    },
    {
      "idVariable": 5,
      "cdSerie": 272,
      "descripcion": "Tipo de Cambio Mayorista ($ por USD) Comunicación A 3500 - Referencia",
      "fecha": "2024-09-20",
      "valor": 965.75
    },
    {
      "idVariable": 6,
      "cdSerie": 7935,
      "descripcion": "Tasa de Política Monetaria (en % n.a.)",
      "fecha": "2024-09-20",
      "valor": 40
    },
    {
      "idVariable": 7,
      "cdSerie": 1222,
      "descripcion": "BADLAR en pesos de bancos privados (en % n.a.)",
      "fecha": "2024-09-19",
      "valor": 40.125
    },
    {
      "idVariable": 8,
      "cdSerie": 7922,
      "descripcion": "TM20 en pesos de bancos privados (en % n.a.)",
      "fecha": "2024-09-19",
      "valor": 41.875
    },
    {
      "idVariable": 9,
      "cdSerie": 7920,
      "descripcion": "Tasas de interés de las operaciones de pase activas para el BCRA, a 1 día de plazo (en % n.a.)",
      "fecha": "2024-09-23",
      "valor": 45
    },
    {
      "idVariable": 10,
      "cdSerie": 7921,
      "descripcion": "Tasas de interés de las operaciones de pase pasivas para el BCRA, a 1 día de plazo (en % n.a.)",
      "fecha": "2024-07-19",
      "valor": 40
    },
    {
      "idVariable": 11,
      "cdSerie": 3139,
      "descripcion": "Tasas de interés por préstamos entre entidades financiera privadas (BAIBAR) (en % n.a.)",
      "fecha": "2024-09-19",
      "valor": 44.59
    },
    {
      "idVariable": 12,
      "cdSerie": 1212,
      "descripcion": "Tasas de interés por depósitos a 30 días de plazo en entidades financieras (en % n.a.)",
      "fecha": "2024-09-19",
      "valor": 39.5
    },
    {
      "idVariable": 13,
      "cdSerie": 7924,
      "descripcion": "Tasa de interés de préstamos por adelantos en cuenta corriente",
      "fecha": "2024-09-19",
      "valor": 48.34
    },
    {
      "idVariable": 14,
      "cdSerie": 7925,
      "descripcion": "Tasa de interés de préstamos personales",
      "fecha": "2024-09-19",
      "valor": 66.08
    },
    {
      "idVariable": 15,
      "cdSerie": 250,
      "descripcion": "Base monetaria - Total (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 23026646
    },
    {
      "idVariable": 16,
      "cdSerie": 251,
      "descripcion": "Circulación monetaria (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 14611221
    },
    {
      "idVariable": 17,
      "cdSerie": 251,
      "descripcion": "Billetes y monedas en poder del público (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 13113134
    },
    {
      "idVariable": 18,
      "cdSerie": 296,
      "descripcion": "Efectivo en entidades financieras (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 1498087
    },
    {
      "idVariable": 19,
      "cdSerie": 252,
      "descripcion": "Depósitos de los bancos en cta. cte. en pesos en el BCRA (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 8415425
    },
    {
      "idVariable": 21,
      "cdSerie": 444,
      "descripcion": "Depósitos en efectivo en las entidades financieras - Total (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 109861851
    },
    {
      "idVariable": 22,
      "cdSerie": 446,
      "descripcion": "En cuentas corrientes (neto de utilización FUCO) (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 20224448
    },
    {
      "idVariable": 23,
      "cdSerie": 450,
      "descripcion": "En Caja de ahorros (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 38669854
    },
    {
      "idVariable": 24,
      "cdSerie": 452,
      "descripcion": "A plazo (incluye inversiones y excluye CEDROS) (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 44318526
    },
    {
      "idVariable": 25,
      "cdSerie": 7919,
      "descripcion": "M2 privado, promedio móvil de 30 días, variación interanual (en %)",
      "fecha": "2024-09-18",
      "valor": 157.6
    },
    {
      "idVariable": 26,
      "cdSerie": 392,
      "descripcion": "Préstamos de las entidades financieras al sector privado (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 46144354
    },
    {
      "idVariable": 27,
      "cdSerie": 7931,
      "descripcion": "Inflación mensual (variación en %)",
      "fecha": "2024-08-31",
      "valor": 4.2
    },
    {
      "idVariable": 28,
      "cdSerie": 7932,
      "descripcion": "Inflación interanual (variación en % i.a.)",
      "fecha": "2024-08-31",
      "valor": 236.7
    },
    {
      "idVariable": 29,
      "cdSerie": 7933,
      "descripcion": "Inflación esperada - REM próximos 12 meses - MEDIANA (variación en % i.a)",
      "fecha": "2024-08-31",
      "valor": 44.7
    },
    {
      "idVariable": 30,
      "cdSerie": 3540,
      "descripcion": "CER (Base 2.2.2002=1)",
      "fecha": "2024-09-23",
      "valor": 464.8495
    },
    {
      "idVariable": 31,
      "cdSerie": 7913,
      "descripcion": "Unidad de Valor Adquisitivo (UVA) (en pesos -con dos decimales-, base 31.3.2016=14.05)",
      "fecha": "2024-09-23",
      "valor": 1169.08
    },
    {
      "idVariable": 32,
      "cdSerie": 7914,
      "descripcion": "Unidad de Vivienda (UVI) (en pesos -con dos decimales-, base 31.3.2016=14.05)",
      "fecha": "2024-09-23",
      "valor": 896.96
    },
    {
      "idVariable": 34,
      "cdSerie": 7936,
      "descripcion": "Tasa de Política Monetaria (en % e.a.)",
      "fecha": "2024-09-20",
      "valor": 49.15
    },
    {
      "idVariable": 35,
      "cdSerie": 7937,
      "descripcion": "BADLAR en pesos de bancos privados (en % e.a.)",
      "fecha": "2024-09-19",
      "valor": 48.34
    },
    {
      "idVariable": 40,
      "cdSerie": 7988,
      "descripcion": "Índice para Contratos de Locación (ICL-Ley 27.551, con dos decimales, base 30.6.20=1)",
      "fecha": "2024-09-23",
      "valor": 18.73
    },
    {
      "idVariable": 41,
      "cdSerie": 7990,
      "descripcion": "Tasas de interés de las operaciones de pase pasivas para el BCRA, a 1 día de plazo (en % e.a.)",
      "fecha": "2024-07-19",
      "valor": 49.15
    },
    {
      "idVariable": 42,
      "cdSerie": 266,
      "descripcion": "Pases pasivos para el BCRA - Saldos (en millones de pesos)",
      "fecha": "2024-09-18",
      "valor": 0
    },
    {
      "idVariable": 43,
      "cdSerie": 3539,
      "descripcion": "Tasa de interés para uso de la Justicia – Comunicado P 14290 | Base 01/04/1991 (en %)",
      "fecha": "2024-09-23",
      "valor": 16571.1395
    }
  ]
}
"""