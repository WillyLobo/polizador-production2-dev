from django.contrib.gis.db import models
from django.db.models import Count, Q

from .base import (
    SRID_GDU, Auditado, EstadoDominial, Lookup, NomenclaturaCatastral, NomenclaturaCatastralOpcional,
)


class Barrio(Auditado):
    intervencion = models.ForeignKey("Intervencion", models.PROTECT, related_name="barrios")
    nombre = models.CharField(max_length=255, blank=True)
    geom = models.MultiPolygonField(srid=SRID_GDU)

    def __str__(self):
        return self.nombre or f"Barrio {self.pk}"

    class Meta:
        permissions = [("ver_barrios", "Puede ver la capa de Barrios")]


class Manzana(Auditado):
    intervencion = models.ForeignKey("Intervencion", models.PROTECT, related_name="manzanas")
    nombre = models.CharField(max_length=255)
    geom = models.PolygonField(srid=SRID_GDU)

    def __str__(self):
        return self.nombre


class Calle(Auditado):
    intervencion = models.ForeignKey("Intervencion", models.PROTECT, related_name="calles")
    nombre = models.CharField(max_length=255, blank=True)
    geom = models.LineStringField(srid=SRID_GDU)

    def __str__(self):
        return self.nombre or f"Calle {self.pk}"


class DestinoParcela(Lookup):
    class Meta(Lookup.Meta):
        verbose_name = "destino de parcela"
        verbose_name_plural = "destinos de parcela"


class ParcelaQuerySet(models.QuerySet):
    def con_es_ph(self):
        # reemplaza la columna es_ph que mantenía el trigger set_es_ph() sobre uf
        return self.annotate(cantidad_ufs=Count("ufs"), es_ph=Q(cantidad_ufs__gt=1))


class Parcela(NomenclaturaCatastral, Auditado):
    intervencion = models.ForeignKey("Intervencion", models.PROTECT, related_name="parcelas")
    destino = models.ForeignKey(DestinoParcela, models.PROTECT, related_name="+")
    estado_dominial = models.CharField(
        max_length=20, choices=EstadoDominial.choices, blank=True,
        help_text="Para reservas y espacios verdes",
    )
    geom = models.PolygonField(srid=SRID_GDU)

    objects = ParcelaQuerySet.as_manager()

    def __str__(self):
        return self.nomenclatura or f"Parcela {self.pk}"

    class Meta:
        indexes = [models.Index(fields=["nomenclatura"], name="gdu_parcela_nomenclatura")]
        # nomenclatura tiene duplicados en la base heredada: la UniqueConstraint se
        # agrega cuando el área los resuelva


class DatosAdjudicatario(models.Model):
    """La base heredada guardaba en nro_adjudicatario un DNI o un número de
    adjudicatario del Sistema 3450 según tipo_id_adjudicatario (muchas veces vacío).
    Acá quedan separados; lo que el ETL no pudo clasificar queda en
    nro_adjudicatario_legacy para revisión manual."""
    dni = models.BigIntegerField("DNI", null=True, blank=True)
    adjudicatario = models.ForeignKey(
        "Adjudicatario3450", models.DO_NOTHING, null=True, blank=True, related_name="+",
        # caché de una API externa que puede ir atrasado respecto de la carga en QGIS
        db_constraint=False,
    )
    nro_adjudicatario_legacy = models.BigIntegerField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True


class Uf(DatosAdjudicatario, Auditado):
    parcela = models.ForeignKey(Parcela, models.PROTECT, related_name="ufs")
    uf = models.CharField("UF", max_length=10)
    poligono = models.CharField("polígono", max_length=255, blank=True)
    coefuf = models.DecimalField("coeficiente", max_digits=10, decimal_places=5, null=True, blank=True)
    nivel = models.IntegerField(null=True, blank=True)
    designacion = models.CharField("designación", max_length=255, blank=True)
    estado_dominial = models.CharField(max_length=20, choices=EstadoDominial.choices, blank=True)
    fr_mat = models.CharField("folio real / matrícula", max_length=255, blank=True)
    res_costos = models.ForeignKey(
        "ResolucionCostos", models.PROTECT, null=True, blank=True, related_name="ufs",
        verbose_name="resolución de costos",
    )
    observaciones = models.CharField(max_length=255, blank=True)
    # obligatoria: si la UF es única en la parcela, es una copia de la geometría de la parcela
    geom = models.PolygonField(srid=SRID_GDU)

    def __str__(self):
        return f"UF {self.uf}"

    class Meta:
        verbose_name = "unidad funcional"
        verbose_name_plural = "unidades funcionales"
        db_table_comment = "Unidad funcional. Depende de una parcela."
        permissions = [
            ("ver_viviendas", "Puede ver la capa de Viviendas"),
            ("ver_escriturar", "Puede ver la capa de Viviendas para Escriturar"),
            ("editar_dominio", "Puede editar el estado dominial de la UF"),
            ("editar_nro_adjudicatario", "Puede editar el número de adjudicatario de la UF"),
        ]


class ViviendaPunto(DatosAdjudicatario, NomenclaturaCatastralOpcional, Auditado):
    intervencion = models.ForeignKey("Intervencion", models.PROTECT, related_name="viviendas_punto")
    estado_dominial = models.CharField(max_length=20, choices=EstadoDominial.choices)
    apellido = models.CharField(max_length=255, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    geom = models.PointField(srid=SRID_GDU)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}" if self.apellido else f"Vivienda {self.pk}"

    class Meta:
        verbose_name = "vivienda dispersa"
        verbose_name_plural = "viviendas dispersas"
        permissions = [("ver_viviendas_dispersas", "Puede ver la capa de Viviendas Dispersas")]


class PreAdjudicatarioDispersa(NomenclaturaCatastralOpcional, Auditado):
    apellido = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    genero = models.CharField("género", max_length=255, blank=True)
    documento = models.BigIntegerField(null=True, blank=True)
    cantidad_personas = models.IntegerField(null=True, blank=True, help_text="Integrantes del grupo familiar")
    inscripcion = models.CharField("inscripción", max_length=255, blank=True)
    plano_mensura = models.ForeignKey(
        "PlanoMensura", models.PROTECT, null=True, blank=True, related_name="pre_adjudicatarios",
    )
    # texto libre original, cuando el ETL no pudo resolverlo a un PlanoMensura
    plano_mensura_legacy = models.CharField(max_length=255, blank=True, editable=False)
    propietario = models.CharField(max_length=255, blank=True)
    apto_dominial = models.CharField(max_length=255, blank=True)
    observaciones = models.TextField(blank=True)
    geom = models.PointField(srid=SRID_GDU)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    class Meta:
        verbose_name = "pre-adjudicatario de vivienda dispersa"
        verbose_name_plural = "pre-adjudicatarios de vivienda dispersa"


class Catastrourbano(models.Model):
    """Catastro urbano provincial: capa de referencia de solo lectura (no se edita
    desde QGIS ni desde Django), se importa tal cual desde la fuente."""
    id_nomencl = models.CharField(max_length=29, blank=True)
    plano_apro = models.CharField(max_length=11, blank=True)
    dpto = models.CharField(max_length=2, blank=True)
    circ = models.CharField(max_length=3, blank=True)
    secc = models.CharField(max_length=2, blank=True)
    ch = models.CharField(max_length=4, blank=True)
    qta = models.CharField(max_length=4, blank=True)
    fracc = models.CharField(max_length=4, blank=True)
    mz = models.CharField(max_length=5, blank=True)
    parc = models.CharField(max_length=5, blank=True)
    matric = models.CharField(max_length=6, blank=True)
    tomo = models.IntegerField(null=True, blank=True)
    folio = models.IntegerField(null=True, blank=True)
    finca = models.IntegerField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    municipio = models.CharField(max_length=254, blank=True)
    geom = models.PolygonField(srid=SRID_GDU, null=True, blank=True)

    def __str__(self):
        return self.id_nomencl or f"Catastro urbano {self.pk}"

    class Meta:
        verbose_name = "parcela de catastro urbano"
        verbose_name_plural = "catastro urbano"
        indexes = [models.Index(fields=["id_nomencl"], name="gdu_catastrourbano_nomencl")]
        permissions = [("ver_catastro_urbano", "Puede ver la capa de Catastro Urbano")]


class ZonaParcelas(models.Model):
    """Zonificación de Resistencia, capa de referencia para QGIS."""
    nombre = models.CharField(max_length=255, blank=True)
    geom = models.MultiPolygonField(srid=SRID_GDU)

    def __str__(self):
        return self.nombre or f"Zona {self.pk}"

    class Meta:
        verbose_name = "zona de parcelas"
        verbose_name_plural = "zonas de parcelas"
