# Generated by Django 5.0.3 on 2024-09-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretariador', '0010_comisionado_comisionado_cargo_decreto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='solicitud_actuacion_jurisdiccion',
            field=models.CharField(default='E10', max_length=3, verbose_name='Jurisdicción'),
        ),
    ]