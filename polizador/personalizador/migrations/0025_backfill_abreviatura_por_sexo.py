from django.db import migrations


def backfill_abreviatura(apps, schema_editor):
    """Completa `abreviatura` (Sr./Sra.) para los registros de Agente y
    ComisionadoExterno que se cargaron sin ese dato, en base a `sexo`
    (mismo criterio Masculino/Femenino que ya se usa en el resto del código
    para "el"/"la"). No pisa abreviaturas ya cargadas."""
    Agente = apps.get_model("personalizador", "Agente")
    ComisionadoExterno = apps.get_model("personalizador", "ComisionadoExterno")

    for modelo in (Agente, ComisionadoExterno):
        for instancia in modelo.objects.filter(abreviatura__isnull=True) | modelo.objects.filter(abreviatura=""):
            instancia.abreviatura = "Sr." if instancia.sexo.generoagente_nombre == "Masculino" else "Sra."
            instancia.save(update_fields=["abreviatura"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("personalizador", "0024_comisionadoexterno_historicalcomisionadoexterno"),
    ]

    operations = [
        migrations.RunPython(backfill_abreviatura, noop),
    ]
