from django.db import migrations


def fix_content_types(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ContentType.objects.filter(app_label='secretariador', model='customuser').update(app_label='personalizador')
    ContentType.objects.filter(app_label='secretariador', model='historicalcustomuser').update(app_label='personalizador')


def reverse_content_types(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ContentType.objects.filter(app_label='personalizador', model='customuser').update(app_label='secretariador')
    ContentType.objects.filter(app_label='personalizador', model='historicalcustomuser').update(app_label='secretariador')


class Migration(migrations.Migration):

    dependencies = [
        ('personalizador', '0003_cargos_cargos_uuid_cargotipo_cargotipo_uuid_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(fix_content_types, reverse_content_types),
    ]
