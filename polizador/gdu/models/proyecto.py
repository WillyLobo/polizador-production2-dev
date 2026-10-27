from django.contrib.gis.db import models

from core.validators import CuitValidator

from .base import Auditado, Lookup, TipoResolucion

# Jerarquía programa -> actuación -> contratación -> intervención. La geografía
# (localidad) se comparte con carga; programa y ejecutor todavía no, hasta que se
# retome la integración con carga.Obra.


class Programa(Auditado):
    class Origen(models.TextChoices):
        NACIONAL = "nacional", "Nacional"
        PROVINCIAL = "provincial", "Provincial"

    nombre = models.CharField(max_length=255)
    origen = models.CharField(max_length=20, choices=Origen.choices, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        db_table_comment = "Origen e instrumentación del financiamiento"


class Actuacion(Auditado):
    programa = models.ForeignKey(Programa, models.PROTECT, related_name="actuaciones")
    ano = models.IntegerField("año")
    nombre = models.CharField(max_length=255)
    instrumento = models.CharField(max_length=255, help_text="Instrumento legal que genera la actuación")

    def __str__(self):
        return f"{self.nombre} ({self.ano})"

    class Meta:
        verbose_name = "actuación"
        verbose_name_plural = "actuaciones"
        db_table_comment = "Expediente matriz por el cual se asignan recursos a contrataciones e intervenciones"


class TipoContratacion(Lookup):
    class Meta(Lookup.Meta):
        verbose_name = "tipo de contratación"
        verbose_name_plural = "tipos de contratación"


class Contratacion(Auditado):
    actuacion = models.ForeignKey(Actuacion, models.PROTECT, related_name="contrataciones", verbose_name="actuación")
    tipo = models.ForeignKey(TipoContratacion, models.PROTECT, related_name="+")
    # la base heredada mezclaba ambos con COALESCE(expediente, resolucion); acá quedan separados
    expediente = models.CharField(max_length=255, blank=True)
    resolucion = models.CharField("resolución", max_length=255, blank=True)
    ano = models.IntegerField("año")
    nombre = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre or self.expediente or self.resolucion or f"Contratación {self.pk}"

    class Meta:
        verbose_name = "contratación"
        verbose_name_plural = "contrataciones"
        db_table_comment = "Acto legal por el que se contrata la ejecución de obras"


class TipoIntervencion(Lookup):
    class Meta(Lookup.Meta):
        verbose_name = "tipo de intervención"
        verbose_name_plural = "tipos de intervención"


class AdjudicacionBeneficiario(Auditado):
    nro = models.CharField(max_length=255)
    ano = models.IntegerField("año")
    tipo = models.CharField(max_length=20, choices=TipoResolucion.choices)

    def __str__(self):
        return f"Adjudicación {self.nro}/{self.ano} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = "adjudicación a beneficiarios"
        verbose_name_plural = "adjudicaciones a beneficiarios"


class ResolucionCostos(Auditado):
    nro_largo = models.IntegerField()
    nro_corto = models.IntegerField()
    ano = models.IntegerField("año")
    tipo = models.CharField(max_length=20, choices=TipoResolucion.choices)

    def __str__(self):
        return f"Resolución {self.nro_largo}/{self.nro_corto} - {self.ano} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = "resolución de costos"
        verbose_name_plural = "resoluciones de costos"
        # (nro_largo, ano) tiene duplicados en la base heredada: la UniqueConstraint
        # se agrega cuando el área los resuelva


class Intervencion(Auditado):
    class Estado(models.TextChoices):
        EVALUACION = "evaluacion", "Evaluación"
        TERMINADA = "terminada", "Terminada"

    contratacion = models.ForeignKey(Contratacion, models.PROTECT, related_name="intervenciones", verbose_name="contratación")
    localidad = models.ForeignKey("carga.Localidad", models.PROTECT, related_name="intervenciones_gdu")
    nombre = models.CharField(max_length=255)
    tipo = models.ForeignKey(TipoIntervencion, models.PROTECT, related_name="+")
    estado = models.CharField(max_length=20, choices=Estado.choices, blank=True)
    avance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Porcentaje")
    plan = models.IntegerField(null=True, blank=True)
    # texto: hay grupos alfanuméricos ("8A"); reemplaza a grupo + drf_grupo de la base heredada
    grupo = models.CharField(max_length=255, blank=True)
    adjudicacion = models.ForeignKey(
        AdjudicacionBeneficiario, models.PROTECT, null=True, blank=True, related_name="intervenciones",
        verbose_name="adjudicación",
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "intervención"
        verbose_name_plural = "intervenciones"
        db_table_comment = "Área real en la que se desarrolla o desarrolló un proyecto"


class TipoEjecutor(Lookup):
    class Meta(Lookup.Meta):
        verbose_name = "tipo de ejecutor"
        verbose_name_plural = "tipos de ejecutor"


class Ejecutor(Auditado):
    tipo = models.ForeignKey(TipoEjecutor, models.PROTECT, related_name="+")
    cuit = models.CharField("CUIT", max_length=11, validators=[CuitValidator()])
    nombre = models.CharField(max_length=255)
    localidad = models.ForeignKey("carga.Localidad", models.PROTECT, null=True, blank=True, related_name="+")
    nombre_contacto = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "ejecutores"
        ordering = ["nombre"]


class Inspector(Lookup):
    class Meta(Lookup.Meta):
        verbose_name_plural = "inspectores"


# N:N explícitas (sin ManyToManyField): django-oapif no maneja M2M directos, cada
# tabla intermedia se publica como colección propia para editarla desde QGIS.

class IntervencionEjecutor(Auditado):
    intervencion = models.ForeignKey(Intervencion, models.CASCADE, related_name="ejecutores", verbose_name="intervención")
    ejecutor = models.ForeignKey(Ejecutor, models.PROTECT, related_name="intervenciones")

    def __str__(self):
        return f"{self.intervencion} - {self.ejecutor}"

    class Meta:
        verbose_name = "ejecutor de intervención"
        verbose_name_plural = "ejecutores de intervención"
        constraints = [
            models.UniqueConstraint(fields=["intervencion", "ejecutor"], name="gdu_intervencion_ejecutor_unico"),
        ]


class IntervencionInspector(Auditado):
    intervencion = models.ForeignKey(Intervencion, models.CASCADE, related_name="inspectores", verbose_name="intervención")
    inspector = models.ForeignKey(Inspector, models.PROTECT, related_name="intervenciones")

    def __str__(self):
        return f"{self.intervencion} - {self.inspector}"

    class Meta:
        verbose_name = "inspector de intervención"
        verbose_name_plural = "inspectores de intervención"
        constraints = [
            models.UniqueConstraint(fields=["intervencion", "inspector"], name="gdu_intervencion_inspector_unico"),
        ]
