from django.contrib.gis.db import models

from .base import SRID_GDU, Auditado, Lookup, NomenclaturaCatastral


class EstadoGestionExpropiacion(Lookup):
    class Meta(Lookup.Meta):
        verbose_name = "estado de gestión de expropiación"
        verbose_name_plural = "estados de gestión de expropiación"


class ObjetoExpropiacion(Lookup):
    class Meta(Lookup.Meta):
        verbose_name = "objeto de expropiación"
        verbose_name_plural = "objetos de expropiación"


class Expropiacion(Auditado):
    class Gestion(models.TextChoices):
        IPDUV = "ipduv", "IPDUV"
        EXTERNA = "externa", "Externa"

    nro_ley = models.IntegerField(help_text="Ley original de expropiación")
    letra_ley = models.CharField(max_length=1, blank=True)
    ano_ley = models.IntegerField("año de la ley", null=True, blank=True)
    ley_prorrogas = models.CharField("prórrogas y modificatorias", max_length=255, blank=True)
    localidad = models.ForeignKey("carga.Localidad", models.PROTECT, related_name="expropiaciones_gdu")
    asentamiento = models.BooleanField(help_text="Indica si tiene asentamiento")
    asentamiento_nombre = models.CharField(max_length=255, blank=True)
    gestion = models.CharField("gestión", max_length=20, choices=Gestion.choices)

    def __str__(self):
        ley = f"{self.nro_ley}{self.letra_ley}"
        return f"Ley {ley}/{self.ano_ley}" if self.ano_ley else f"Ley {ley}"

    class Meta:
        verbose_name = "expropiación"
        verbose_name_plural = "expropiaciones"


class ParcelaExpropiada(NomenclaturaCatastral, Auditado):
    expropiacion = models.ForeignKey(Expropiacion, models.PROTECT, related_name="parcelas", verbose_name="expropiación")
    objeto = models.ForeignKey(ObjetoExpropiacion, models.PROTECT, related_name="+")
    estado_gestion = models.ForeignKey(EstadoGestionExpropiacion, models.PROTECT, related_name="+", verbose_name="estado de gestión")
    propietario_expropiado = models.CharField(max_length=255, blank=True)
    propietario_actual = models.CharField(max_length=255, blank=True, help_text="Luego de la expropiación")
    inscripcion = models.CharField("inscripción", max_length=255, blank=True)
    regularizable = models.BooleanField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    geom = models.PolygonField(srid=SRID_GDU)

    def __str__(self):
        return self.nomenclatura or f"Parcela expropiada {self.pk}"

    class Meta:
        verbose_name_plural = "parcelas expropiadas"
        permissions = [("ver_expropiaciones", "Puede ver la capa de Expropiaciones")]
