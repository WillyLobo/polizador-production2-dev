from django.db import migrations


def copiar_mes_pct_a_anticipo_pct(apps, schema_editor):
    Certificado = apps.get_model("carga", "Certificado")
    anticipos = Certificado.objects.filter(certificado_tipo="ANTICIPO")
    for certificado in anticipos:
        certificado.certificado_anticipo_pct = certificado.certificado_mes_pct
        certificado.certificado_mes_pct = 0
        certificado.save(update_fields=["certificado_anticipo_pct", "certificado_mes_pct"])


def revertir(apps, schema_editor):
    Certificado = apps.get_model("carga", "Certificado")
    anticipos = Certificado.objects.filter(certificado_tipo="ANTICIPO")
    for certificado in anticipos:
        certificado.certificado_mes_pct = certificado.certificado_anticipo_pct
        certificado.certificado_anticipo_pct = 0
        certificado.save(update_fields=["certificado_anticipo_pct", "certificado_mes_pct"])


class Migration(migrations.Migration):

    dependencies = [
        ('carga', '0038_certificado_certificado_anticipo_pct_and_more'),
    ]

    operations = [
        migrations.RunPython(copiar_mes_pct_a_anticipo_pct, revertir),
    ]
