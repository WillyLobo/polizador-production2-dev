from django.contrib.gis.db import models

# managed=False: tablas/vistas de la base GDU heredada (migrada desde el proyecto hasura),
# el schema real vive fuera del control de las migraciones de Django.


class Encuesta(models.Model):
    relevamiento = models.ForeignKey('Relevamiento', models.DO_NOTHING, db_column='relevamiento')
    # FK compuesta real en Postgres: (vivienda, relevamiento) -> our.vivienda(vivienda, relevamiento).
    # Django no soporta FK de múltiples columnas, se modela como campo simple.
    vivienda = models.IntegerField(db_comment='referencia a la vivienda en la tabla UF. Agregar mas adelante la FK')
    user = models.CharField(blank=True, null=True, db_comment='usuario que cargó la encuesta')
    tstamp = models.DateTimeField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True, db_comment='tipo de encuesta (app mobile, presencial, telefónica, otros)')

    def __str__(self):
        return f"Encuesta #{self.pk} (vivienda {self.vivienda})"

    class Meta:
        managed = False
        db_table = '"our"."encuesta"'


class GjRegistros(models.Model):
    gj = models.TextField(primary_key=True)  # This field type is a guess.

    def __str__(self):
        return self.gj

    class Meta:
        managed = False
        db_table = '"our"."gj_registros"'


class Pregunta(models.Model):
    tipo = models.ForeignKey('TipoPregunta', models.DO_NOTHING, db_column='tipo')
    texto = models.TextField(db_comment='Texto principal de la pregunta')
    subtexto = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.texto[:60]

    class Meta:
        managed = False
        db_table = '"our"."pregunta"'


class PreguntaRelevamiento(models.Model):
    relevamiento = models.ForeignKey('Relevamiento', models.DO_NOTHING, db_column='relevamiento')
    seccion = models.ForeignKey('Seccion', models.DO_NOTHING, db_column='seccion')
    pregunta = models.ForeignKey('Pregunta', models.DO_NOTHING, db_column='pregunta')
    variable = models.CharField(max_length=255, db_comment='indica el nombre de la variable dentro del objeto encuesta para ser referenciado por las reglas')
    visible = models.TextField(blank=True, null=True, db_comment='regla en JS que indica si la pregunta es visible (recibe como argumento la encuesta)')
    valido = models.TextField(blank=True, null=True, db_comment='regla en JS que indica si la respuesta a la pregunta es valida (recibe como argumento la encuesta)')
    required = models.BooleanField()

    def __str__(self):
        return self.variable

    class Meta:
        managed = False
        db_table = '"our"."pregunta_relevamiento"'
        unique_together = (('relevamiento', 'variable'),)


class Relevamiento(models.Model):
    nombre = models.CharField(max_length=255)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    objetivo = models.IntegerField(db_comment='cantidad objetivo de encuestas a realizar, para calcular porcentaje de avance')
    viviendas = models.JSONField(blank=True, null=True, db_comment='(Geo)JSON con la capa de viviendas y sus datos asociados')
    barrios = models.JSONField(blank=True, null=True, db_comment='(Geo)JSON con la capa de barrios y sus datos asociados')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"our"."relevamiento"'
        db_table_comment = 'Representa a un grupo de encuestas a ser realizadas en alguna campaña'
        permissions = [("encuestar_relevamiento", "Puede cargar encuestas de un relevamiento")]


class Respuesta(models.Model):
    pregunta = models.ForeignKey('Pregunta', models.DO_NOTHING, db_column='pregunta')
    texto = models.CharField(max_length=255)
    nro_opcion = models.IntegerField(db_comment='valor numérico a devolver en la variable, sirve para ordenar además')
    valor = models.TextField(db_comment='valor textual a devolver en la variable')

    def __str__(self):
        return self.texto

    class Meta:
        managed = False
        db_table = '"our"."respuesta"'
        unique_together = (('pregunta', 'nro_opcion'),)
        db_table_comment = 'una de las posibles respuestas a una pregunta (especialmente para multiple choice)'


class RespuestaEncuesta(models.Model):
    encuesta = models.ForeignKey('Encuesta', models.DO_NOTHING, db_column='encuesta')
    pregunta = models.ForeignKey('PreguntaRelevamiento', models.DO_NOTHING, db_column='pregunta')
    respuesta = models.ForeignKey('Respuesta', models.DO_NOTHING, db_column='respuesta', blank=True, null=True)
    valor = models.TextField()

    def __str__(self):
        return f"Respuesta encuesta #{self.encuesta_id} - pregunta {self.pregunta_id}"

    class Meta:
        managed = False
        db_table = '"our"."respuesta_encuesta"'
        db_table_comment = 'respuesta a una pregunta puntual de una encuesta'


class ResultadosEncuesta(models.Model):
    id_pregunta = models.IntegerField(primary_key=True)
    variable = models.CharField(max_length=255, blank=True, null=True)
    encuesta = models.IntegerField(blank=True, null=True)
    valor = models.TextField(blank=True, null=True)
    tipo_dato = models.CharField(max_length=255, blank=True, null=True)
    tipo_pregunta = models.IntegerField(blank=True, null=True)
    respuesta = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.variable or f"Resultado #{self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"our"."resultados_encuesta"'


class ResultadosPregunta(models.Model):
    pregunta = models.IntegerField(primary_key=True)
    id_respuesta = models.IntegerField(blank=True, null=True)
    valor = models.TextField(blank=True, null=True)
    respuesta = models.TextField(blank=True, null=True)
    cantidad = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.respuesta or f"Resultado pregunta #{self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"our"."resultados_pregunta"'


class Seccion(models.Model):
    relevamiento = models.ForeignKey('Relevamiento', models.DO_NOTHING, db_column='relevamiento')
    nombre = models.CharField(max_length=255)
    texto = models.TextField(blank=True, null=True)
    orden = models.IntegerField()
    visible = models.TextField(blank=True, null=True, db_comment='regla en JS que indica si la seccion es visible (recibe como argumento la encuesta)')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"our"."seccion"'


class TipoPregunta(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, db_comment='indica el tipo de dato de la respuesta')
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"our"."tipo_pregunta"'


class VariablesEncuesta(models.Model):
    id_pregunta = models.IntegerField(primary_key=True)
    variable = models.CharField(max_length=255, blank=True, null=True)
    tipo_dato = models.CharField(max_length=255, blank=True, null=True)
    tipo_pregunta = models.IntegerField(blank=True, null=True)
    respuestas = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return self.variable or f"Variable #{self.pk}"

    class Meta:
        managed = False
        db_table = '"our"."variables_encuesta"'


class Vivienda(models.Model):
    relevamiento = models.ForeignKey('Relevamiento', models.DO_NOTHING, db_column='relevamiento')
    vivienda = models.IntegerField()
    geom = models.MultiPolygonField(srid=3857)
    properties = models.JSONField()
    relevado = models.BooleanField()

    def __str__(self):
        return f"Vivienda {self.vivienda} (relevamiento {self.relevamiento_id})"

    class Meta:
        managed = False
        db_table = '"our"."vivienda"'
        unique_together = (('relevamiento', 'vivienda'),)

