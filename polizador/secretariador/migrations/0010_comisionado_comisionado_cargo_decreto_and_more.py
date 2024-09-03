# Generated by Django 5.0.3 on 2024-09-03 12:39

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalizador', '0001_initial'),
        ('secretariador', '0009_solicitud_solicitud_anulada_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comisionado',
            name='comisionado_cargo_decreto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cargo_decreto', to='personalizador.cargos', verbose_name='Cargo Decreto'),
        ),
        migrations.AddField(
            model_name='comisionado',
            name='comisionado_cargo_interno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cargo_interno', to='personalizador.cargos', verbose_name='Cargo Interno'),
        ),
        migrations.AddField(
            model_name='comisionado',
            name='comisionado_cargo_interno_resolucion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='secretariador.instrumentoslegalesresoluciones'),
        ),
        migrations.AddField(
            model_name='comisionado',
            name='comisionado_verificado_contra_padron',
            field=models.BooleanField(default=False, verbose_name='Chequeado'),
        ),
        migrations.AlterField(
            model_name='comisionado',
            name='comisionado_dni',
            field=models.DecimalField(decimal_places=0, max_digits=9, unique=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='DNI:'),
        ),
    ]
