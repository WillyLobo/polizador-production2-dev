# Generated by Django 5.0.3 on 2024-09-12 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretariador', '0011_solicitud_solicitud_actuacion_jurisdiccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='comisionadosolicitud',
            name='comisionadosolicitud_sin_viatico',
            field=models.BooleanField(default=False, verbose_name='Sin viático'),
        ),
    ]
