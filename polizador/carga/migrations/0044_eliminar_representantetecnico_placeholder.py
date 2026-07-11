from django.db import migrations

PLACEHOLDER_ID = 3


def limpiar_placeholder(apps, schema_editor):
    RepresentanteTecnico = apps.get_model("personalizador", "RepresentanteTecnico")
    try:
        placeholder = RepresentanteTecnico.objects.get(pk=PLACEHOLDER_ID)
    except RepresentanteTecnico.DoesNotExist:
        return
    placeholder.obra_representantetecnico.clear()
    placeholder.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('carga', '0043_obra_inspector_representantetecnico_blank'),
    ]

    operations = [
        migrations.RunPython(limpiar_placeholder, migrations.RunPython.noop),
    ]
