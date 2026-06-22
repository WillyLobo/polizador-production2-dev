from django.db import migrations, models

NEW_FK_CONSTRAINT = "carga_obra_obra_inspector_agente_id_fk_personalizador_agente"


class Migration(migrations.Migration):
    """
    Phase 3: ids are now correct personalizador.Agente ids (0010), so add the
    real FK constraint back (pointing at personalizador_agente) and update
    Django's model state to match. The constraint is added via raw SQL
    (separate from Django's own AlterField SQL generation) because Django has
    no clean way to retarget a ManyToManyField's FK constraint without trying
    to validate against the old table first.
    """

    dependencies = [
        ('carga', '0010_obra_inspector_remap_data'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        f'ALTER TABLE carga_obra_obra_inspector ADD CONSTRAINT "{NEW_FK_CONSTRAINT}" '
                        'FOREIGN KEY (agente_id) REFERENCES personalizador_agente(id) DEFERRABLE INITIALLY DEFERRED'
                    ),
                    reverse_sql=f'ALTER TABLE carga_obra_obra_inspector DROP CONSTRAINT "{NEW_FK_CONSTRAINT}"',
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='obra',
                    name='obra_inspector',
                    field=models.ManyToManyField(related_name='obra_inspector', to='personalizador.agente', verbose_name='Inspector'),
                ),
            ],
        ),
    ]
