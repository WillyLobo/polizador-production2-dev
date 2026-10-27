from django.contrib.gis.db import models

from .base import SRID_GDU, Auditado, Lookup, NomenclaturaCatastral


class TipoVinculoPlano(models.TextChoices):
    PERIMETRAL = "perimetral", "Perimetral"
    SUBDIVISION = "subdivision", "Subdivisión"


class PlanoMensura(Auditado):
    depto = models.CharField(max_length=2, help_text="Código de departamento (parte del identificador)")
    nro = models.IntegerField(help_text="Número asignado por Catastro (parte del identificador)")
    ano = models.CharField("año", max_length=2, help_text="Año, 2 dígitos (parte del identificador)")
    pm_antecedente = models.CharField("plano antecedente", max_length=255, blank=True)
    en_gdu = models.BooleanField("en GDU", null=True, blank=True, help_text="El plano se encuentra en la Gerencia")
    sup_parcelas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sup_calles = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sup_reserva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    geom = models.PolygonField(srid=SRID_GDU, null=True, blank=True)

    def __str__(self):
        return f"{self.depto}-{self.nro}-{self.ano}"

    class Meta:
        verbose_name = "plano de mensura"
        verbose_name_plural = "planos de mensura"
        indexes = [models.Index(fields=["depto", "nro", "ano"], name="gdu_planomensura_ident")]
        # (depto, nro, ano) tiene duplicados en la base heredada: la UniqueConstraint
        # se agrega cuando el área los resuelva
        permissions = [("ver_plano_mensura", "Puede ver la capa de Planos de Mensura")]


class PlanoMensuraIntervencion(Auditado):
    plano = models.ForeignKey(PlanoMensura, models.CASCADE, related_name="intervenciones")
    intervencion = models.ForeignKey("Intervencion", models.CASCADE, related_name="planos")
    tipo = models.CharField(max_length=20, choices=TipoVinculoPlano.choices)

    def __str__(self):
        return f"{self.plano} - {self.intervencion} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = "plano de intervención"
        verbose_name_plural = "planos de intervención"
        constraints = [
            models.UniqueConstraint(fields=["plano", "intervencion", "tipo"], name="gdu_plano_intervencion_unico"),
        ]


class TierraDestino(Lookup):
    class Meta(Lookup.Meta):
        verbose_name = "destino de tierra"
        verbose_name_plural = "destinos de tierra"


class TipoDocProbatoria(Lookup):
    class Meta(Lookup.Meta):
        verbose_name = "tipo de documentación probatoria"
        verbose_name_plural = "tipos de documentación probatoria"


class Tierra(NomenclaturaCatastral, Auditado):
    class Tipo(models.TextChoices):
        IPDUV = "ipduv", "IPDUV"
        TERCEROS = "terceros", "Terceros"

    class TipoOferente(models.TextChoices):
        PROVINCIA = "provincia", "Provincia"
        MUNICIPIO = "municipio", "Municipio"
        ENTIDAD_INTERMEDIA = "entidad_intermedia", "Entidad intermedia"
        PARTICULAR = "particular", "Particular"

    class TipoInscripcion(models.TextChoices):
        FOLIO_REAL = "folio_real", "Folio real"
        TOMO_FOLIO_FINCA_ANO = "tomo_folio_finca_ano", "Tomo, folio, finca y año"
        ARTICULO_LEY = "articulo_ley", "Artículo de ley"

    class Localizacion(models.TextChoices):
        CENTRAL = "central", "Central"
        INTERMEDIA = "intermedia", "Intermedia"
        PERIFERICA = "periferica", "Periférica"

    class Superficie(models.TextChoices):
        HASTA_200 = "0-200", "0 a 200 m²"
        DE_200_A_500 = "200-500", "200 a 500 m²"
        MAS_DE_500 = "500+", "Más de 500 m²"

    class EstadoOcupacion(models.TextChoices):
        LIBRE = "libre", "Libre"
        PARCIALMENTE_OCUPADO = "parcialmente_ocupado", "Parcialmente ocupado"
        OCUPADO = "ocupado", "Ocupado"

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    tipo_oferente = models.CharField(max_length=20, choices=TipoOferente.choices)
    oferente = models.CharField(max_length=255, blank=True)
    propietario = models.CharField(max_length=255, blank=True)
    localidad = models.ForeignKey("carga.Localidad", models.PROTECT, null=True, blank=True, related_name="+")
    tipo_inscripcion = models.CharField("tipo de inscripción", max_length=30, choices=TipoInscripcion.choices, blank=True)
    inscripcion = models.CharField("inscripción", max_length=255, blank=True)
    tipo_doc_probatoria = models.ForeignKey(TipoDocProbatoria, models.PROTECT, null=True, blank=True, related_name="+")
    apto_fisico = models.BooleanField("apto físico", null=True, blank=True)
    apto_dominial = models.BooleanField(null=True, blank=True)
    apto_localizacion = models.BooleanField("apto localización", null=True, blank=True)
    visita_campo = models.BooleanField("visita de campo", null=True, blank=True)
    visita_profesional = models.CharField(max_length=255, blank=True)
    visita_fecha = models.DateField(null=True, blank=True)
    localizacion = models.CharField("localización", max_length=20, choices=Localizacion.choices, blank=True)
    superficie = models.CharField(max_length=10, choices=Superficie.choices, blank=True)
    proyecto_loteo = models.BooleanField("proyecto de loteo", null=True, blank=True)
    estado = models.CharField(max_length=30, choices=EstadoOcupacion.choices, blank=True)
    destino = models.ForeignKey(TierraDestino, models.PROTECT, null=True, blank=True, related_name="+")
    otro_destino = models.CharField(max_length=255, blank=True)
    observaciones = models.TextField(blank=True)
    geom = models.PolygonField(srid=SRID_GDU)

    def __str__(self):
        return self.propietario or self.nomenclatura or f"Tierra {self.pk}"

    class Meta:
        verbose_name_plural = "tierras"


class TierraConsulta(Auditado):
    """Una consulta a un área (inundabilidad, dominio, municipio, ...) sobre una tierra.
    Reemplaza las 27 columnas <area>_solicitado/_respuesta/_observaciones de la base
    heredada."""

    class Area(models.TextChoices):
        INUNDABILIDAD = "inundabilidad", "Inundabilidad"
        DOMINIO = "dominio", "Dominio"
        MUNICIPAL = "municipal", "Municipal"
        TASACIONES = "tasaciones", "Tasaciones"
        LYT = "lyt", "Loteos y tierras"
        PROYECTOS = "proy", "Proyectos"
        SOCIAL = "social", "Social"
        INFORME = "informe", "Informe"
        INFRAESTRUCTURA = "infraestructura", "Infraestructura"

    tierra = models.ForeignKey(Tierra, models.CASCADE, related_name="consultas")
    area = models.CharField("área", max_length=20, choices=Area.choices)
    solicitado = models.CharField(max_length=255, blank=True)
    respuesta = models.CharField(max_length=255, blank=True)
    resolucion = models.CharField("resolución", max_length=255, blank=True)
    observaciones = models.CharField(max_length=255, blank=True)
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, help_text="Solo tasaciones")

    def __str__(self):
        return f"{self.tierra} - {self.get_area_display()}"

    class Meta:
        verbose_name = "consulta sobre tierra"
        verbose_name_plural = "consultas sobre tierras"
        constraints = [models.UniqueConstraint(fields=["tierra", "area"], name="gdu_tierra_consulta_unica")]


class PlanoMensuraTierra(Auditado):
    plano = models.ForeignKey(PlanoMensura, models.CASCADE, related_name="tierras")
    tierra = models.ForeignKey(Tierra, models.CASCADE, related_name="planos")
    tipo = models.CharField(max_length=20, choices=TipoVinculoPlano.choices)

    def __str__(self):
        return f"{self.plano} - {self.tierra} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = "plano de tierra"
        verbose_name_plural = "planos de tierras"
        constraints = [
            models.UniqueConstraint(fields=["plano", "tierra", "tipo"], name="gdu_plano_tierra_unico"),
        ]
