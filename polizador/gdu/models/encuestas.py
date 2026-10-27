from django.conf import settings
from django.contrib.gis.db import models
from django.db.models import Exists, OuterRef
from uuid_utils import compat

from .base import SRID_GDU

# Constructor de encuestas (modelo EAV): relevamiento -> sección -> pregunta ->
# respuesta. Las reglas de visibilidad/validez eran expresiones JS guardadas como
# texto; acá son reglas declarativas (JSON) que se validan del lado del servidor.


class TipoPregunta(models.Model):
    # los ids se conservan de la base heredada: el formulario los usa para decidir el widget
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, help_text="Tipo de dato de la respuesta")
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipo de pregunta"
        verbose_name_plural = "tipos de pregunta"


class Relevamiento(models.Model):
    nombre = models.CharField(max_length=255)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    objetivo = models.IntegerField(help_text="Cantidad objetivo de encuestas, para calcular el avance")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table_comment = "Grupo de encuestas a realizar en una campaña"
        permissions = [("encuestar_relevamiento", "Puede cargar encuestas de un relevamiento")]


class Seccion(models.Model):
    relevamiento = models.ForeignKey(Relevamiento, models.CASCADE, related_name="secciones")
    nombre = models.CharField(max_length=255)
    texto = models.TextField(blank=True)
    orden = models.IntegerField()
    regla_visible = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "sección"
        verbose_name_plural = "secciones"
        ordering = ["relevamiento", "orden"]


class Pregunta(models.Model):
    tipo = models.ForeignKey(TipoPregunta, models.PROTECT, related_name="+")
    texto = models.TextField()
    subtexto = models.TextField(blank=True)

    def __str__(self):
        return self.texto[:60]


class PreguntaRelevamiento(models.Model):
    relevamiento = models.ForeignKey(Relevamiento, models.CASCADE, related_name="preguntas")
    seccion = models.ForeignKey(Seccion, models.CASCADE, related_name="preguntas")
    pregunta = models.ForeignKey(Pregunta, models.PROTECT, related_name="usos")
    variable = models.CharField(max_length=255, help_text="Nombre con el que las reglas referencian la respuesta")
    regla_visible = models.JSONField(null=True, blank=True)
    regla_valido = models.JSONField(null=True, blank=True)
    requerida = models.BooleanField(default=False)

    def __str__(self):
        return self.variable

    class Meta:
        verbose_name = "pregunta de relevamiento"
        verbose_name_plural = "preguntas de relevamiento"
        constraints = [
            models.UniqueConstraint(fields=["relevamiento", "variable"], name="gdu_pregunta_relevamiento_variable"),
        ]


class Respuesta(models.Model):
    """Opción posible de una pregunta (multiple choice)."""
    pregunta = models.ForeignKey(Pregunta, models.CASCADE, related_name="opciones")
    texto = models.CharField(max_length=255)
    nro_opcion = models.IntegerField(help_text="Valor numérico de la opción, también define el orden")
    valor = models.TextField()

    def __str__(self):
        return self.texto

    class Meta:
        ordering = ["pregunta", "nro_opcion"]
        constraints = [
            models.UniqueConstraint(fields=["pregunta", "nro_opcion"], name="gdu_respuesta_opcion_unica"),
        ]


class ViviendaRelevamientoQuerySet(models.QuerySet):
    def con_relevado(self):
        # reemplaza la columna relevado que mantenía el trigger update_vivienda_relevado()
        return self.annotate(relevado=Exists(Encuesta.objects.filter(vivienda=OuterRef("pk"))))


class ViviendaRelevamiento(models.Model):
    relevamiento = models.ForeignKey(Relevamiento, models.CASCADE, related_name="viviendas")
    numero = models.IntegerField(help_text="Identificador de la vivienda dentro del relevamiento")
    uf = models.ForeignKey("Uf", models.SET_NULL, null=True, blank=True, related_name="viviendas_relevamiento")
    # foto de los datos de la vivienda (adjudicatario, grupo, manzana, ...) al armar el relevamiento
    datos = models.JSONField(default=dict, blank=True)
    geom = models.MultiPolygonField(srid=SRID_GDU)

    objects = ViviendaRelevamientoQuerySet.as_manager()

    def __str__(self):
        return f"Vivienda {self.numero} ({self.relevamiento})"

    class Meta:
        verbose_name = "vivienda de relevamiento"
        verbose_name_plural = "viviendas de relevamiento"
        constraints = [
            models.UniqueConstraint(fields=["relevamiento", "numero"], name="gdu_vivienda_relevamiento_unica"),
        ]


class Encuesta(models.Model):
    class Tipo(models.IntegerChoices):
        APP_MOBILE = 1, "App mobile"
        PRESENCIAL = 2, "Presencial"
        TELEFONICA = 3, "Telefónica"
        OTROS = 4, "Otros"
        WEB = 5, "Formulario web"

    # generado en el cliente, para poder reintentar envíos sin duplicar (carga offline)
    uuid = models.UUIDField(default=compat.uuid7, unique=True, editable=False)
    relevamiento = models.ForeignKey(Relevamiento, models.PROTECT, related_name="encuestas")
    vivienda = models.ForeignKey(ViviendaRelevamiento, models.PROTECT, related_name="encuestas")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, related_name="+")
    # username de la base heredada cuando no se pudo resolver a un usuario
    usuario_legacy = models.CharField(max_length=255, blank=True, editable=False)
    tipo = models.PositiveSmallIntegerField(choices=Tipo.choices, null=True, blank=True)
    capturada_en = models.DateTimeField(null=True, blank=True, help_text="Momento de la carga en campo")
    enviada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Encuesta #{self.pk} ({self.vivienda})"


class RespuestaEncuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta, models.CASCADE, related_name="respuestas")
    pregunta_relevamiento = models.ForeignKey(PreguntaRelevamiento, models.PROTECT, related_name="respuestas")
    respuesta = models.ForeignKey(Respuesta, models.PROTECT, null=True, blank=True, related_name="+")
    valor = models.TextField()

    def __str__(self):
        return f"Encuesta #{self.encuesta_id} - {self.pregunta_relevamiento}"

    class Meta:
        verbose_name = "respuesta de encuesta"
        verbose_name_plural = "respuestas de encuesta"
