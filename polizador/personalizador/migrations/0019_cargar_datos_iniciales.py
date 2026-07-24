from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import migrations


def cargar_datos_iniciales(apps, schema_editor):
    call_command("fill_fields")
    call_command("crear_oficinas")
    try:
        call_command("importar_agentes_padron")
    except CommandError as exc:
        print(f"importar_agentes_padron: salteado ({exc})")


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("personalizador", "0018_alter_agente_cargo_interno_and_more"),
    ]

    operations = [
        migrations.RunPython(cargar_datos_iniciales, noop),
    ]
