from django.contrib.gis.db import models


class Adjudicatario3450(models.Model):
    """Caché local del Sistema 3450 (Gob. del Chaco), lo refresca importar_3450. La PK es
    el número de adjudicatario de ese sistema. Absorbe catastro.tmp_regularizacion
    (estado_regularizacion) y reemplaza las columnas "AdjuGIS*" de la base heredada."""
    nro_adjudicatario = models.IntegerField(primary_key=True)
    apellido_nombre = models.CharField(max_length=255, blank=True)
    dni = models.BigIntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    escritura = models.BooleanField(null=True, blank=True, help_text="Escriturada según el Sistema 3450")
    matricula = models.CharField(max_length=255, blank=True)
    res_nro = models.IntegerField(null=True, blank=True)
    res_fecha = models.DateField(null=True, blank=True)
    res_acta = models.CharField(max_length=255, blank=True)
    motivo = models.CharField(max_length=255, blank=True)
    situacion = models.CharField(max_length=255, blank=True)
    estado_regularizacion = models.CharField(max_length=255, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.apellido_nombre or f"Adjudicatario {self.nro_adjudicatario}"

    class Meta:
        verbose_name = "adjudicatario (Sistema 3450)"
        verbose_name_plural = "adjudicatarios (Sistema 3450)"
