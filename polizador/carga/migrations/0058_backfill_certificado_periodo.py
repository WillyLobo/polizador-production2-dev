from django.db import migrations


def backfill_periodo(apps, schema_editor):
    """Certificados generados desde una Foja antes de que la generación cargara
    certificado_periodo: se completa con el mes de la Foja ("MM/AAAA", formato legacy)."""
    Certificado = apps.get_model("carga", "Certificado")
    pendientes = Certificado.objects.filter(
        certificado_periodo__isnull=True, certificado_foja__isnull=False
    ).select_related("certificado_foja")
    for certificado in pendientes:
        Certificado.objects.filter(pk=certificado.pk).update(
            certificado_periodo=certificado.certificado_foja.foja_periodo.strftime("%m/%Y")
        )


class Migration(migrations.Migration):

    dependencies = [
        ("carga", "0057_obra_fecha_inicio"),
    ]

    operations = [
        migrations.RunPython(backfill_periodo, migrations.RunPython.noop),
    ]
