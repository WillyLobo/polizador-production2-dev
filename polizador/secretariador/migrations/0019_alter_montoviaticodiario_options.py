# Generated by Django 5.0.3 on 2025-05-22 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secretariador', '0018_comisionado_comisionado_personal_de_gabinete'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='montoviaticodiario',
            options={'get_latest_by': ['montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_ano', 'montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_numero'], 'ordering': ['montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_ano', 'montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_numero'], 'verbose_name': 'Monto diario de Viático', 'verbose_name_plural': 'Monto diario de Viáticos'},
        ),
    ]
