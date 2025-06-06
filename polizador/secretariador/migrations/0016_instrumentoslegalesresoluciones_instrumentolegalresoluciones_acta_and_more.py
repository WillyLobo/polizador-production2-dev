# Generated by Django 5.0.3 on 2025-04-28 13:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretariador', '0015_alter_instrumentoslegalesmemorandum_instrumentolegalmemorandum_autocarga'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrumentoslegalesresoluciones',
            name='instrumentolegalresoluciones_acta',
            field=models.CharField(default='', max_length=3, verbose_name='Acta'),
        ),
        migrations.AlterField(
            model_name='incorporacion',
            name='incorporacion_actuacion_ano',
            field=models.DecimalField(decimal_places=0, default=2025, max_digits=4, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Año Actuación'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='solicitud_actuacion_ano',
            field=models.DecimalField(decimal_places=0, default=2025, max_digits=4, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Año Actuación'),
        ),
    ]
