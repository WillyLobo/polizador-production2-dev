from django.db import migrations


class Migration(migrations.Migration):
    """
    Final phase: carga.Agente has no more incoming references (0011 finished
    the obra_inspector repoint) and its data has already been copied into
    personalizador.Agente by personalizador's 0011 data migration. Safe to
    drop it entirely.
    """

    dependencies = [
        ('carga', '0011_obra_inspector_restore_constraint'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Agente',
        ),
        migrations.DeleteModel(
            name='HistoricalAgente',
        ),
    ]
