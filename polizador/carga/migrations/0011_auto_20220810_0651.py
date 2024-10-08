# Generated by Django 3.2.4 on 2022-08-10 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carga', '0010_alter_obra_obra_conjunto_licitado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_numero', models.CharField(max_length=10, verbose_name='Número Región')),
            ],
            options={
                'verbose_name_plural': 'Region',
                'ordering': ['region_numero'],
            },
        ),
        migrations.AddField(
            model_name='obra',
            name='obra_departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carga.departamento'),
        ),
        migrations.AddField(
            model_name='obra',
            name='obra_departamento_m',
            field=models.ManyToManyField(related_name='obra_departamento', to='carga.Departamento'),
        ),
        migrations.AddField(
            model_name='obra',
            name='obra_localidad_m',
            field=models.ManyToManyField(related_name='obra_localidad', to='carga.Localidad'),
        ),
        migrations.AddField(
            model_name='obra',
            name='obra_municipio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carga.municipio'),
        ),
        migrations.AddField(
            model_name='obra',
            name='obra_municipio_m',
            field=models.ManyToManyField(related_name='obra_municipio', to='carga.Municipio'),
        ),
        migrations.AlterField(
            model_name='aseguradora',
            name='aseguradora_nombre',
            field=models.CharField(max_length=255, verbose_name='Nombre Empresa Aseguradora'),
        ),
        migrations.AddField(
            model_name='municipio',
            name='municipio_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='carga.region'),
        ),
        migrations.AddField(
            model_name='obra',
            name='obra_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carga.region'),
        ),
    ]
