from django.db import migrations


def borrar_tipos_del_piloto(apps, schema_editor):
    # en cascada: sus permisos, las asignaciones a grupos y usuarios, y el log del admin
    ContentType = apps.get_model("contenttypes", "ContentType")
    ContentType.objects.using(schema_editor.connection.alias).filter(app_label="gdu_piloto").delete()


class Migration(migrations.Migration):
    """La app transitoria gdu_piloto ya no existe: se borra lo que dejó en la base. Su única
    tabla propia era el vínculo obra-contratación (vacío, nunca se usó); el resto de sus
    modelos eran managed=False sobre los schemas de la base heredada, que no son de Django."""

    dependencies = [
        ("gdu", "0003_nomenclatura_nula_y_verbose_names"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("admin", "0003_logentry_add_action_flag_choices"),
        ("personalizador", "0032_agente_retirado_jubilado_fallecido"),
    ]

    operations = [
        migrations.RunSQL("DROP TABLE IF EXISTS gdu_piloto_obracontratacion", migrations.RunSQL.noop),
        migrations.RunSQL("DELETE FROM django_migrations WHERE app = 'gdu_piloto'", migrations.RunSQL.noop),
        migrations.RunPython(borrar_tipos_del_piloto, migrations.RunPython.noop),
    ]
