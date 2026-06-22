import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Phase 3 of the FK repoint: ids are now correct personalizador.Agente ids
    (0005), so retarget the fields to personalizador.Agente and restore the
    real DB constraint (db_constraint defaults back to True).
    """

    dependencies = [
        ('secretariador', '0005_agente_fk_remap_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='vehiculo_titular_agente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personalizador.agente'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='solicitud_solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personalizador.agente'),
        ),
        migrations.AlterField(
            model_name='comisionadosolicitud',
            name='comisionadosolicitud_nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personalizador.agente'),
        ),
        migrations.AlterField(
            model_name='incorporacion',
            name='incorporacion_solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personalizador.agente'),
        ),
    ]
