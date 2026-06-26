from decimal import Decimal

from django.db import migrations
from django.db.models import Max, Sum
from django.utils import timezone

# Código corto de CertificadoFinanciamiento -> prefijo de los campos de Obra.
FUENTES = (("N", "nacion"), ("P", "provincia"), ("T", "terceros"))


def reconciliar_montos_contrato(apps, schema_editor):
    """
    Hasta ahora obra_contrato_{nacion,provincia,terceros}_{pesos,uvi,uvi_fecha} se
    tipeaban a mano en Obra. A partir de esta serie de cambios pasan a calcularse
    como la suma/fecha-más-reciente de los ContratoMonto de los Contratos de la obra.

    En la base real, la mayoría de las Obras ya coincide exactamente con esa suma,
    pero un subconjunto no (incluye Obras sin ningún Contrato cargado). Para esas,
    se crea un Contrato+ContratoMonto "legado" con la diferencia necesaria, de forma
    que la nueva fuente derivada reproduzca el valor que ya se le mostraba al usuario
    -- sin esto, esas Obras pasarían a mostrar $0 o un monto menor de la nada.
    """
    Obra = apps.get_model("carga", "Obra")
    Contrato = apps.get_model("carga", "Contrato")
    ContratoMonto = apps.get_model("carga", "ContratoMonto")
    CertificadoFinanciamiento = apps.get_model("carga", "CertificadoFinanciamiento")
    CertificadoRubro = apps.get_model("carga", "CertificadoRubro")

    financiamiento_by_codigo = {
        f.certificadofinanciamiento_nombre_corto: f
        for f in CertificadoFinanciamiento.objects.filter(
            certificadofinanciamiento_nombre_corto__in=["N", "P", "T"]
        )
    }
    # "Vivienda" es el rubro que ya usa la carga automática de contratos legados.
    rubro_legado = (
        CertificadoRubro.objects.filter(certificadorubro_nombre="Vivienda").first()
        or CertificadoRubro.objects.order_by("pk").first()
    )
    if not financiamiento_by_codigo or rubro_legado is None:
        # Entorno sin los datos base de financiamiento/rubro (p.ej. tests): nada para reconciliar.
        return

    pendientes_de_revisar = []

    for obra in Obra.objects.all().iterator():
        montos_obra = ContratoMonto.objects.filter(contratomonto_contrato__contrato_obra=obra)
        contrato_legado = None

        for codigo, prefijo in FUENTES:
            financiamiento = financiamiento_by_codigo.get(codigo)
            if financiamiento is None:
                continue

            agregado = montos_obra.filter(contratomonto_financiamiento_id=financiamiento.pk).aggregate(
                pesos=Sum("contratomonto_pesos"), uvi=Sum("contratomonto_uvi")
            )
            pesos_actual = Decimal(getattr(obra, f"obra_contrato_{prefijo}_pesos") or 0)
            uvi_actual = Decimal(getattr(obra, f"obra_contrato_{prefijo}_uvi") or 0)
            diff_pesos = pesos_actual - Decimal(agregado["pesos"] or 0)
            diff_uvi = uvi_actual - Decimal(agregado["uvi"] or 0)

            if diff_pesos == 0 and diff_uvi == 0:
                continue

            if contrato_legado is None:
                contrato_legado = Contrato.objects.create(
                    contrato_obra=obra,
                    contrato_fecha=obra.obra_fecha_contrato or timezone.now().date(),
                    contrato_descripcion="Migración: reconciliación de montos históricos",
                    contrato_autocarga=True,
                )

            ContratoMonto.objects.create(
                contratomonto_contrato=contrato_legado,
                contratomonto_rubro=rubro_legado,
                contratomonto_financiamiento=financiamiento,
                contratomonto_pesos=diff_pesos,
                contratomonto_uvi=diff_uvi,
                contratomonto_uvi_fecha=getattr(obra, f"obra_contrato_{prefijo}_uvi_fecha"),
            )

        # Verificación defensiva: con la diferencia recién insertada, la suma de
        # ContratoMonto debería volver a coincidir exactamente con los campos actuales.
        montos_obra = ContratoMonto.objects.filter(contratomonto_contrato__contrato_obra=obra)
        for codigo, prefijo in FUENTES:
            financiamiento = financiamiento_by_codigo.get(codigo)
            agregado = montos_obra.filter(contratomonto_financiamiento_id=getattr(financiamiento, "pk", None)).aggregate(
                pesos=Sum("contratomonto_pesos"), uvi=Sum("contratomonto_uvi")
            )
            pesos_actual = Decimal(getattr(obra, f"obra_contrato_{prefijo}_pesos") or 0)
            uvi_actual = Decimal(getattr(obra, f"obra_contrato_{prefijo}_uvi") or 0)
            if pesos_actual != Decimal(agregado["pesos"] or 0) or uvi_actual != Decimal(agregado["uvi"] or 0):
                pendientes_de_revisar.append(obra.pk)

    if pendientes_de_revisar:
        print(
            f"\n[0021_reconciliar_montos_contrato] ATENCIÓN: {len(pendientes_de_revisar)} "
            f"Obra(s) siguen sin coincidir con la suma de ContratoMonto, revisar manualmente: "
            f"{sorted(set(pendientes_de_revisar))}"
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("carga", "0020_historicalplandetrabajosrubro_rubro_documento_digital_and_more"),
    ]

    operations = [
        migrations.RunPython(reconciliar_montos_contrato, noop),
    ]
