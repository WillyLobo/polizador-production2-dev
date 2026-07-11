from django.contrib.gis.db import models

# managed=False: tablas/vistas de la base GDU heredada (migrada desde el proyecto hasura),
# el schema real vive fuera del control de las migraciones de Django.


class Area(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"visualizador"."area"'
        db_table_comment = 'Areas del IPDUV'


class Barrios(models.Model):
    programa = models.CharField(max_length=255, blank=True, null=True)
    actuacion = models.CharField(max_length=255, blank=True, null=True)
    instrumento = models.CharField(max_length=255, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=255, blank=True, null=True)
    contratacion = models.CharField(max_length=255, blank=True, null=True)
    tipo_contratacion = models.CharField(max_length=255, blank=True, null=True)
    obra = models.CharField(max_length=255, blank=True, null=True)
    tipo_obra = models.CharField(max_length=255, blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)
    barrio = models.CharField(max_length=255, blank=True, null=True)
    geom = models.MultiPolygonField(srid=22175, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    ejecutores = models.TextField(blank=True, null=True)
    planos = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.barrio or f"Barrio {self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"visualizador"."barrios"'
        permissions = [("ver_barrios", "Puede ver la capa de Barrios")]


class Calles(models.Model):
    programa = models.CharField(max_length=255, blank=True, null=True)
    actuacion = models.CharField(max_length=255, blank=True, null=True)
    instrumento = models.CharField(max_length=255, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=255, blank=True, null=True)
    contratacion = models.CharField(max_length=255, blank=True, null=True)
    tipo_contratacion = models.CharField(max_length=255, blank=True, null=True)
    obra = models.CharField(max_length=255, blank=True, null=True)
    tipo_obra = models.CharField(max_length=255, blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)
    calle = models.CharField(max_length=255, blank=True, null=True)
    geom = models.LineStringField(srid=22175, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    ejecutores = models.TextField(blank=True, null=True)
    planos = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.calle or f"Calle {self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"visualizador"."calles"'


class Expropiaciones(models.Model):
    ley = models.TextField(blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)
    dpto = models.CharField(max_length=2, blank=True, null=True)
    circ = models.CharField(max_length=3, blank=True, null=True)
    secc = models.CharField(max_length=2, blank=True, null=True)
    ch = models.CharField(max_length=4, blank=True, null=True)
    qta = models.CharField(max_length=4, blank=True, null=True)
    fracc = models.CharField(max_length=4, blank=True, null=True)
    mz = models.CharField(max_length=4, blank=True, null=True)
    parc = models.CharField(max_length=5, blank=True, null=True)
    folio = models.CharField(max_length=255, blank=True, null=True)
    objeto = models.CharField(max_length=255, blank=True, null=True)
    propietario_expropiado = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PolygonField(srid=22175, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    gestion = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return self.objeto or self.ley or f"Expropiación {self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"visualizador"."expropiaciones"'
        permissions = [("ver_expropiaciones", "Puede ver la capa de Expropiaciones")]


class Manzanas(models.Model):
    programa = models.CharField(max_length=255, blank=True, null=True)
    actuacion = models.CharField(max_length=255, blank=True, null=True)
    instrumento = models.CharField(max_length=255, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=255, blank=True, null=True)
    contratacion = models.CharField(max_length=255, blank=True, null=True)
    tipo_contratacion = models.CharField(max_length=255, blank=True, null=True)
    obra = models.CharField(max_length=255, blank=True, null=True)
    tipo_obra = models.CharField(max_length=255, blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)
    manzana = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PolygonField(srid=22175, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    ejecutores = models.TextField(blank=True, null=True)
    planos = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.manzana or f"Manzana {self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"visualizador"."manzanas"'


class Role(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    group = models.ForeignKey('Rolegroup', models.DO_NOTHING, db_column='group')
    objeto = models.CharField(max_length=255)
    permiso = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"visualizador"."role"'


class Rolegroup(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"visualizador"."rolegroup"'


class Rolemapping(models.Model):
    user = models.ForeignKey('VisualizadorUser', models.DO_NOTHING, db_column='user')
    role = models.ForeignKey('Role', models.DO_NOTHING, db_column='role')
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('VisualizadorUser', models.DO_NOTHING, db_column='created_by', related_name='rolemapping_created_by_set', blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.role}"

    class Meta:
        managed = False
        db_table = '"visualizador"."rolemapping"'
        unique_together = (('user', 'role'),)


class VisualizadorUser(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    email = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey('self', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    activo = models.BooleanField()
    area = models.ForeignKey('Area', models.DO_NOTHING, db_column='area', blank=True, null=True)
    tokenm = models.CharField(max_length=255, blank=True, null=True, db_comment='token para la app mobile')

    def __str__(self):
        return self.nombre or self.username or f"Usuario #{self.pk}"

    class Meta:
        managed = False
        db_table = '"visualizador"."user"'
        permissions = [("admin_gdu_usuarios", "Puede administrar usuarios de GDU")]


class ViviendaDispersa(models.Model):
    programa = models.CharField(max_length=255, blank=True, null=True)
    actuacion = models.CharField(max_length=255, blank=True, null=True)
    instrumento = models.CharField(max_length=255, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=255, blank=True, null=True)
    contratacion = models.CharField(max_length=255, blank=True, null=True)
    tipo_contratacion = models.CharField(max_length=255, blank=True, null=True)
    obra = models.CharField(max_length=255, blank=True, null=True)
    plan = models.IntegerField(blank=True, null=True)
    grupo = models.IntegerField(blank=True, null=True)
    tipo_obra = models.CharField(max_length=255, blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)
    dpto = models.CharField(max_length=2, blank=True, null=True)
    circ = models.CharField(max_length=3, blank=True, null=True)
    secc = models.CharField(max_length=2, blank=True, null=True)
    ch = models.CharField(max_length=4, blank=True, null=True)
    qta = models.CharField(max_length=4, blank=True, null=True)
    fracc = models.CharField(max_length=4, blank=True, null=True)
    mz = models.CharField(max_length=4, blank=True, null=True)
    parc = models.CharField(max_length=5, blank=True, null=True)
    adjudicacion = models.TextField(blank=True, null=True)
    res_costos = models.TextField(blank=True, null=True)
    geom = models.PointField(srid=22175, blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    ejecutores = models.TextField(blank=True, null=True)
    planos = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.obra or f"Vivienda dispersa {self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"visualizador"."vivienda_dispersa"'
        permissions = [("ver_viviendas_dispersas", "Puede ver la capa de Viviendas Dispersas")]


class Viviendas(models.Model):
    programa = models.CharField(max_length=255, blank=True, null=True)
    actuacion = models.CharField(max_length=255, blank=True, null=True)
    instrumento = models.CharField(max_length=255, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=255, blank=True, null=True)
    contratacion = models.CharField(max_length=255, blank=True, null=True)
    tipo_contratacion = models.CharField(max_length=255, blank=True, null=True)
    obra = models.CharField(max_length=255, blank=True, null=True)
    plan = models.IntegerField(blank=True, null=True)
    grupo = models.IntegerField(blank=True, null=True)
    tipo_obra = models.CharField(max_length=255, blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)
    dpto = models.CharField(max_length=2, blank=True, null=True)
    circ = models.CharField(max_length=3, blank=True, null=True)
    secc = models.CharField(max_length=2, blank=True, null=True)
    ch = models.CharField(max_length=4, blank=True, null=True)
    qta = models.CharField(max_length=4, blank=True, null=True)
    fracc = models.CharField(max_length=4, blank=True, null=True)
    mz = models.CharField(max_length=4, blank=True, null=True)
    parc = models.CharField(max_length=5, blank=True, null=True)
    uf = models.CharField(max_length=255, blank=True, null=True)
    tipo_uf = models.CharField(max_length=255, blank=True, null=True)
    estado_dominial = models.TextField(blank=True, null=True)  # This field type is a guess.
    nro_adjudicatario = models.BigIntegerField(blank=True, null=True)
    tipo_id_adjudicatario = models.TextField(blank=True, null=True)  # This field type is a guess.
    fr_mat = models.CharField(max_length=255, blank=True, null=True)
    adjudicacion = models.TextField(blank=True, null=True)
    res_costos = models.TextField(blank=True, null=True)
    geom = models.PolygonField(srid=22175, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    ejecutores = models.TextField(blank=True, null=True)
    planos = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.uf or f"Vivienda {self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"visualizador"."viviendas"'
        permissions = [("ver_viviendas", "Puede ver la capa de Viviendas")]


class ViviendasPh(models.Model):
    id = models.IntegerField(primary_key=True)
    programa = models.CharField(max_length=255, blank=True, null=True)
    actuacion = models.CharField(max_length=255, blank=True, null=True)
    instrumento = models.CharField(max_length=255, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=255, blank=True, null=True)
    contratacion = models.CharField(max_length=255, blank=True, null=True)
    tipo_contratacion = models.CharField(max_length=255, blank=True, null=True)
    obra = models.CharField(max_length=255, blank=True, null=True)
    plan = models.IntegerField(blank=True, null=True)
    grupo = models.IntegerField(blank=True, null=True)
    tipo_obra = models.CharField(max_length=255, blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)
    id_parcela = models.IntegerField(blank=True, null=True)
    dpto = models.CharField(max_length=2, blank=True, null=True)
    circ = models.CharField(max_length=3, blank=True, null=True)
    secc = models.CharField(max_length=2, blank=True, null=True)
    ch = models.CharField(max_length=4, blank=True, null=True)
    qta = models.CharField(max_length=4, blank=True, null=True)
    fracc = models.CharField(max_length=4, blank=True, null=True)
    mz = models.CharField(max_length=4, blank=True, null=True)
    parc = models.CharField(max_length=5, blank=True, null=True)
    uf = models.CharField(max_length=10, blank=True, null=True)
    coefuf = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    designacion = models.CharField(max_length=255, blank=True, null=True)
    poligono = models.CharField(max_length=255, blank=True, null=True)
    tipo_uf = models.CharField(max_length=255, blank=True, null=True)
    estado_dominial = models.TextField(blank=True, null=True)  # This field type is a guess.
    nro_adjudicatario = models.BigIntegerField(blank=True, null=True)
    tipo_id_adjudicatario = models.TextField(blank=True, null=True)  # This field type is a guess.
    fr_mat = models.CharField(max_length=255, blank=True, null=True)
    adjudicacion = models.TextField(blank=True, null=True)
    res_costos = models.TextField(blank=True, null=True)
    adjudicatario3450 = models.CharField(max_length=255, blank=True, null=True)
    escritura3450 = models.CharField(max_length=2, blank=True, null=True)
    situacion3450 = models.CharField(max_length=255, blank=True, null=True)
    motivo3450 = models.CharField(max_length=255, blank=True, null=True)
    matricula3450 = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PolygonField(srid=22175, blank=True, null=True)
    ejecutores = models.TextField(blank=True, null=True)
    planos = models.TextField(blank=True, null=True)
    nivel = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.uf or f"Vivienda PH {self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"visualizador"."viviendas_ph"'

