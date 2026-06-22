from django.db import migrations


class Migration(migrations.Migration):
    """
    Final phase of the merge: Comisionado has no more incoming FKs (0005/0006
    repointed them all to personalizador.Agente) and its data has already been
    copied into personalizador.Agente by personalizador's 0011 data migration.
    Safe to drop it entirely.
    """

    dependencies = [
        ('secretariador', '0006_agente_fk_restore_constraint'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='comisionado',
            name='unique_comisionado_1',
        ),
        migrations.RemoveField(
            model_name='comisionado',
            name='comisionado_cargo',
        ),
        migrations.RemoveField(
            model_name='comisionado',
            name='comisionado_cargo_interno_resolucion',
        ),
        migrations.DeleteModel(
            name='HistoricalComisionado',
        ),
        migrations.DeleteModel(
            name='Comisionado',
        ),
    ]
