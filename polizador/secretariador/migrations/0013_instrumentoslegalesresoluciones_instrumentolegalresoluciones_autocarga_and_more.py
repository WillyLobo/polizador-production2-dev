# Generated by Django 5.0.3 on 2024-09-16 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretariador', '0012_comisionadosolicitud_comisionadosolicitud_sin_viatico'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrumentoslegalesresoluciones',
            name='instrumentolegalresoluciones_autocarga',
            field=models.BooleanField(default=False, verbose_name='Resolución importada sin intervención.'),
        ),
        migrations.AddField(
            model_name='instrumentoslegalesresoluciones',
            name='instrumentolegalresoluciones_document',
            field=models.TextField(blank=True, null=True, verbose_name='Texto Extraído por OCR'),
        ),
        migrations.AlterField(
            model_name='incorporacion',
            name='incorporacion_resolucion',
            field=models.ForeignKey(blank=True, help_text='Resolución que aprueba la incorporación de los agentes.', null=True, on_delete=django.db.models.deletion.CASCADE, to='secretariador.instrumentoslegalesresoluciones', verbose_name='Resolución Aprobada'),
        ),
        migrations.AlterField(
            model_name='incorporacion',
            name='incorporacion_solicitud',
            field=models.ForeignKey(help_text='Actuación a la que se incorpora los agentes.', on_delete=django.db.models.deletion.CASCADE, to='secretariador.solicitud'),
        ),
    ]
