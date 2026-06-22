import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Phase 1 of repointing the 4 FKs that used to target secretariador.Comisionado
    to personalizador.Agente instead. The real (non-historical) FK columns still
    hold old Comisionado ids here, so the DB constraint is dropped first
    (db_constraint=False) without changing `to=` yet -- the actual id remap and
    constraint restoration happens in 0005, once it's safe to write
    personalizador.Agente ids into these columns. Historical FK fields already
    have db_constraint=False (simple_history's default) so they can be
    repointed directly with no data-safety concern.
    """

    dependencies = [
        ('personalizador', '0012_agente_merge_data'),
        ('secretariador', '0003_remove_comisionado_comisionado_cargo_decreto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='vehiculo_titular_agente',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='secretariador.comisionado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='solicitud_solicitante',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='secretariador.comisionado'),
        ),
        migrations.AlterField(
            model_name='comisionadosolicitud',
            name='comisionadosolicitud_nombre',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='secretariador.comisionado'),
        ),
        migrations.AlterField(
            model_name='incorporacion',
            name='incorporacion_solicitante',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='secretariador.comisionado'),
        ),
        migrations.AlterField(
            model_name='historicalvehiculo',
            name='vehiculo_titular_agente',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='personalizador.agente'),
        ),
        migrations.AlterField(
            model_name='historicalsolicitud',
            name='solicitud_solicitante',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='personalizador.agente'),
        ),
        migrations.AlterField(
            model_name='historicalcomisionadosolicitud',
            name='comisionadosolicitud_nombre',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='personalizador.agente'),
        ),
        migrations.AlterField(
            model_name='historicalincorporacion',
            name='incorporacion_solicitante',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='personalizador.agente'),
        ),
    ]
