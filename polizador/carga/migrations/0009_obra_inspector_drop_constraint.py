from django.db import migrations

OLD_FK_CONSTRAINT = "carga_obra_obra_inspector_agente_id_587c5d74_fk_carga_agente_id"


class Migration(migrations.Migration):
    """
    Phase 1 of repointing Obra.obra_inspector from carga.Agente to
    personalizador.Agente: drop the FK constraint on the through table's
    agente_id column so it can be written with personalizador.Agente ids in
    0010, which don't exist in carga_agente.
    """

    dependencies = [
        ('carga', '0008_alter_contratosdigitales_contratodigital_archivo_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=f'ALTER TABLE carga_obra_obra_inspector DROP CONSTRAINT "{OLD_FK_CONSTRAINT}"',
            reverse_sql=(
                f'ALTER TABLE carga_obra_obra_inspector ADD CONSTRAINT "{OLD_FK_CONSTRAINT}" '
                'FOREIGN KEY (agente_id) REFERENCES carga_agente(id) DEFERRABLE INITIALLY DEFERRED'
            ),
        ),
    ]
