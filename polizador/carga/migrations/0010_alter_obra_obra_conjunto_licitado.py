# Generated by Django 3.2.4 on 2022-07-06 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carga', '0009_subconjuntolicitado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obra',
            name='obra_conjunto_licitado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='carga.subconjuntolicitado', verbose_name='ConjuntoLicitado'),
        ),
    ]
