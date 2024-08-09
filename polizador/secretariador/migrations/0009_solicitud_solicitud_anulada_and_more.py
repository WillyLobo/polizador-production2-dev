# Generated by Django 5.0.3 on 2024-08-09 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretariador', '0008_comisionadosolicitud_comisionadosolicitud_cantidad_de_dias_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='solicitud_anulada',
            field=models.BooleanField(default=False, help_text='Si la solicitud se encuentra anulada, no se registra en los reportes.', verbose_name='Anulada'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='solicitud_tareas',
            field=models.TextField(help_text='... a fin de #Texto ingresado en el formulario# en la localidad de #Localidad#', verbose_name='Tareas a Realizar'),
        ),
    ]
