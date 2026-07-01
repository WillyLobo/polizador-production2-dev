from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga', '0024_cerrar_contrato_fk_documentos_digitales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalresolucionesdigitales',
            name='resoluciondigital_numero',
            field=models.CharField(max_length=15, verbose_name='Número de Resolución:'),
        ),
        migrations.AlterField(
            model_name='resolucionesdigitales',
            name='resoluciondigital_numero',
            field=models.CharField(max_length=15, verbose_name='Número de Resolución:'),
        ),
    ]
