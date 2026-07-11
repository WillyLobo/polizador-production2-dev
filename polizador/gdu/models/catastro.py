from django.contrib.gis.db import models

# managed=False: tablas/vistas de la base GDU heredada (migrada desde el proyecto hasura),
# el schema real vive fuera del control de las migraciones de Django.


class Actuacion(models.Model):
    id_programa = models.ForeignKey('Programa', models.DO_NOTHING, db_column='id_programa')
    ano = models.IntegerField(db_comment='Año de la actuación')
    nombre = models.CharField(max_length=255, db_comment='Nombre por el cual se conoce a la actuación')
    instrumento = models.CharField(max_length=255, db_comment='Identificador del Instrumento legal que genera la actuación.')
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.ano})"

    class Meta:
        managed = False
        db_table = '"catastro"."actuacion"'
        db_table_comment = 'Representa el expediente matriz por el cual se realiza la asignación de recursos para las distintas contrataciones e intervenciones'


class Adjudicatario3450(models.Model):
    adjugisnroadju = models.IntegerField(db_column='AdjuGISNroAdju', primary_key=True)  # Field name made lowercase.
    adjugisescritura = models.CharField(db_column='AdjuGISEscritura', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adjugisresacta = models.CharField(db_column='AdjuGISResActa', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugisresfecha = models.DateField(db_column='AdjuGISResFecha', blank=True, null=True)  # Field name made lowercase.
    adjugisresnro = models.IntegerField(db_column='AdjuGISResNro', blank=True, null=True)  # Field name made lowercase.
    adjugisapeynom = models.CharField(db_column='AdjuGISapeynom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugisdireccion = models.CharField(db_column='AdjuGISdireccion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugisdni = models.IntegerField(db_column='AdjuGISdni', blank=True, null=True)  # Field name made lowercase.
    adjugismatricula = models.CharField(db_column='AdjuGISmatricula', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugismotivo = models.CharField(db_column='AdjuGISmotivo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugissituacion = models.CharField(db_column='AdjuGISsituacion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugisestadoreg = models.CharField(db_column='AdjuGISEstadoReg', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.adjugisapeynom or f"Adjudicatario {self.adjugisnroadju}"

    class Meta:
        managed = False
        db_table = '"catastro"."adjudicatario3450"'


class Barrio(models.Model):
    id_intervencion = models.ForeignKey('Intervencion', models.DO_NOTHING, db_column='id_intervencion')
    nombre = models.CharField(max_length=255, blank=True, null=True, db_comment='Nombre del barrio')
    geom = models.MultiPolygonField(srid=22175)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre or f"Barrio {self.pk}"

    class Meta:
        managed = False
        db_table = '"catastro"."barrio"'
        db_table_comment = 'Representa el polígono de un barrio creado por una intervención.'


class Catastrourbano(models.Model):
    id_nomencl = models.CharField(max_length=29, blank=True, null=True)
    plano_apro = models.CharField(max_length=11, blank=True, null=True)
    dpto = models.CharField(max_length=2, blank=True, null=True)
    circ = models.CharField(max_length=3, blank=True, null=True)
    secc = models.CharField(max_length=2, blank=True, null=True)
    ch = models.CharField(max_length=4, blank=True, null=True)
    qta = models.CharField(max_length=4, blank=True, null=True)
    fracc = models.CharField(max_length=4, blank=True, null=True)
    mz = models.CharField(max_length=5, blank=True, null=True)
    parc = models.CharField(max_length=5, blank=True, null=True)
    matric = models.CharField(max_length=6, blank=True, null=True)
    tomo = models.IntegerField(blank=True, null=True)
    folio = models.IntegerField(blank=True, null=True)
    finca = models.IntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    municipio = models.CharField(max_length=254, blank=True, null=True)
    geom = models.PolygonField(srid=22175, blank=True, null=True)

    def __str__(self):
        return self.id_nomencl or f"Catastro urbano {self.pk}"

    class Meta:
        managed = False
        db_table = '"catastro"."catastrourbano"'
        permissions = [("ver_catastro_urbano", "Puede ver la capa de Catastro Urbano")]


class Contratacion(models.Model):
    id_actuacion = models.ForeignKey('Actuacion', models.DO_NOTHING, db_column='id_actuacion')
    tipo = models.ForeignKey('TipoContratacion', models.DO_NOTHING, db_column='tipo', db_comment='Tipología de Contratación. (Lic. Pub., Lic. Priv, Conc. Precios, Adj. Directa, etc.)')
    expediente = models.CharField(max_length=255, blank=True, null=True, db_comment='Nro. de expediente, de existir')
    resolucion = models.CharField(max_length=255, blank=True, null=True, db_comment='Nro. de Resolución')
    ano = models.IntegerField(db_comment='Año de la contratación')
    nombre = models.CharField(max_length=255, blank=True, null=True, db_comment='Nombre por el cual se denomina la contratación.')
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre or self.expediente or f"Contratación {self.pk}"

    class Meta:
        managed = False
        db_table = '"catastro"."contratacion"'
        db_table_comment = 'Acto legal mediante el cual se contrata la ejecución de obras (Licitaciones, Concursos, Adj. Directa)'


class EstadoGestionExpropiacion(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"catastro"."estado_gestion_expropiacion"'
        db_table_comment = 'Tipos de Situación Dominial de las parcelas expropiadas:\nEscriturado: (Provincia, IPDUV, MDUT)\nNo Escriturado: (Con Toma, Sin Toma)'


class Expropiacion(models.Model):
    nro_ley = models.IntegerField(db_comment='Ley original de expropiación. Puede tener prórrogas o modificatorias (en ley_prorrogas)')
    ano_ley = models.IntegerField(blank=True, null=True, db_comment='Año de la ley original')
    ley_prorrogas = models.CharField(max_length=255, blank=True, null=True, db_comment='prórrogas y modificatorias subsiguientes de la ley original ( en campo: nro_ley)')
    localidad = models.ForeignKey('Localidad', models.DO_NOTHING, db_column='localidad', db_comment='id de localidad (C. Foránea)')
    asentamiento_nombre = models.CharField(max_length=255, blank=True, null=True, db_comment='Nombre del asentamiento, en caso de tenerlo')
    letra_ley = models.CharField(max_length=1, blank=True, null=True, db_comment='Letra de la ley')
    asentamiento = models.BooleanField(db_comment='Indica si tiene asentamiento')
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    gestion = models.TextField()  # This field type is a guess.

    def __str__(self):
        return f"Ley {self.nro_ley}" + (f"/{self.ano_ley}" if self.ano_ley else "")

    class Meta:
        managed = False
        db_table = '"catastro"."expropiacion"'
        db_table_comment = 'Representa una Ley de Expropiación'


class Intervencion(models.Model):
    id_localidad = models.ForeignKey('Localidad', models.DO_NOTHING, db_column='id_localidad')
    id_contratacion = models.ForeignKey('Contratacion', models.DO_NOTHING, db_column='id_contratacion')
    nombre = models.CharField(max_length=255, db_comment='Nombre para designar a la intervención')
    tipo = models.ForeignKey('TipoIntervencion', models.DO_NOTHING, db_column='tipo', db_comment='Tipología de Intervención.')
    avance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_comment='Avance de la obra, en porcentaje.')
    estado = models.ForeignKey('TipoEstado', models.DO_NOTHING, db_column='estado', blank=True, null=True, db_comment='en obra, paralizada, finalizada, cancelada???')
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    grupo = models.CharField(max_length=255, blank=True, null=True)
    drf_plan = models.IntegerField(blank=True, null=True)
    drf_grupo = models.IntegerField(blank=True, null=True)
    id_adjudicacion = models.ForeignKey('AdjudicacionBeneficiario', models.DO_NOTHING, db_column='id_adjudicacion', blank=True, null=True, db_comment='FK de Resolucion de Adjudicacion')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"catastro"."intervencion"'
        db_table_comment = 'Indica el área real en el que se desarrolla o ha desarrollado un determinado proyecto'


class PlanoMensura(models.Model):
    depto = models.CharField(max_length=2, db_comment='código de depto. Componente del identificador del plano.')
    nro = models.IntegerField(db_comment='Nro de plano asignado por Catastro.  Componente del identificador del plano.')
    ano = models.CharField(max_length=2, db_comment='Año del plano. Componente del identificador del plano.')
    pm_antecedente = models.CharField(max_length=255, blank=True, null=True, db_comment='nro de plano antecedente. Identificador completo')
    en_gdu = models.BooleanField(blank=True, null=True, db_comment='indica si el plano se encuentra en la Gerencia.')
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sup_parcelas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sup_calles = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sup_reserva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    geom = models.PolygonField(srid=22175, blank=True, null=True)

    def __str__(self):
        return self.pm_antecedente or f"{self.depto}-{self.nro}-{self.ano}"

    class Meta:
        managed = False
        db_table = '"catastro"."plano_mensura"'
        db_table_comment = 'Representa el plano de mensura aprobado. depto, nro y ano son los componentes del identificador. '
        permissions = [("ver_plano_mensura", "Puede ver la capa de Planos de Mensura")]


class Programa(models.Model):
    nombre = models.CharField(max_length=255, db_comment='Nombre del Programa')
    origen = models.CharField(max_length=255, db_comment='Origen del programa (Nacional, Provincial, etc)\n')
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fiinancia = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"catastro"."programa"'
        db_table_comment = 'Representa el origen e instrumentación del financiamiento'


class Uf(models.Model):
    id_parcela = models.ForeignKey('Parcela', models.DO_NOTHING, db_column='id_parcela', db_comment='Identificador de parcela (Clave foránea)')
    uf = models.CharField(max_length=10, db_comment='Identificador de la Unidad Funcional')
    coefuf = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, db_comment='Coeficiente de la UF')
    poligono = models.CharField(max_length=255, blank=True, null=True, db_comment='Identificador de Polígono de la UF')
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PolygonField(srid=22175, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    res_costos = models.ForeignKey('ResolucionCostos', models.DO_NOTHING, db_column='res_costos', blank=True, null=True)
    tipo = models.ForeignKey('TipoUf', models.DO_NOTHING, db_column='tipo')
    designacion = models.CharField(max_length=255, blank=True, null=True)
    irregular = models.BooleanField(db_comment='indica si la UF tiene alguna irregularidad dominial')
    estado_dominial = models.TextField(blank=True, null=True)  # This field type is a guess.
    nro_adjudicatario = models.BigIntegerField(blank=True, null=True)
    tipo_id_adjudicatario = models.TextField(blank=True, null=True)  # This field type is a guess.
    fr_mat = models.CharField(max_length=255, blank=True, null=True, db_comment='Folio Real / Matrícula')
    nivel = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"UF {self.uf}"

    class Meta:
        managed = False
        db_table = '"catastro"."uf"'
        db_table_comment = 'Representa una Unidad Funcional. Depende de una parcela. En caso de ser única dentro de la parcela, tiene por defecto la misma forma geométrica.'
        permissions = [
            ("editar_dominio", "Puede editar el estado dominial de la UF"),
            ("editar_nro_adjudicatario", "Puede editar el número de adjudicatario de la UF"),
        ]


class AdjudicacionBeneficiario(models.Model):
    nro = models.CharField(max_length=255, db_comment='nro de la resolución de adjudicación')
    ano = models.IntegerField(db_comment='año de la adjudicación')
    tipo = models.TextField(db_comment='Tipología de adjudicación (provisoria, definitiva)')  # This field type is a guess.
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Adjudicación {self.nro}/{self.ano}"

    class Meta:
        managed = False
        db_table = '"catastro"."adjudicacion_beneficiario"'
        db_table_comment = 'Representa la resolución que adjudica una o mas viviendas a beneficiarios'


class DestinoParcela(models.Model):
    nombre = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"catastro"."destino_parcela"'
        db_table_comment = 'Tipología del destino de la parcela (vivienda, reserva municipal, etc.)'


class Localidad(models.Model):
    codpcia = models.CharField(max_length=2, db_comment='Codigo de provincia segun indec')
    coddpto = models.CharField(max_length=3, db_comment='Codigo de depto segun INDEC')
    codloc = models.CharField(max_length=3, db_comment='Codigo de Localidad segun INDEC')
    provincia = models.CharField(max_length=255, db_comment='Nombre Provincia')
    departamento = models.CharField(max_length=255, db_comment='Nopmbre Departamento')
    localidad = models.CharField(max_length=255, db_comment='Nombre Localidad')
    geom = models.PointField(srid=22175)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.localidad}, {self.departamento}"

    class Meta:
        managed = False
        db_table = '"catastro"."localidad"'
        db_table_comment = 'Localidades según tabla del INDEC'


class Parcela(models.Model):
    id_intervencion = models.ForeignKey('Intervencion', models.DO_NOTHING, db_column='id_intervencion')
    nomenclatura = models.CharField(max_length=28, blank=True, null=True, db_comment='Nomenclatura Catastral completa')
    dpto = models.CharField(max_length=2)
    circ = models.CharField(max_length=3)
    secc = models.CharField(max_length=2)
    ch = models.CharField(max_length=4)
    qta = models.CharField(max_length=4)
    fracc = models.CharField(max_length=4)
    mz = models.CharField(max_length=4)
    parc = models.CharField(max_length=5)
    geom = models.PolygonField(srid=22175)
    destino = models.ForeignKey('DestinoParcela', models.DO_NOTHING, db_column='destino', db_comment='Indica el destino de la parcela (vivienda, reserva municipal, etc.)')
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    estado_dominial = models.TextField(blank=True, null=True, db_comment='Estado Dominial de la Parcela, para el caso de Reservas y Espacios Verdes')  # This field type is a guess.
    es_ph = models.BooleanField()

    def __str__(self):
        return self.nomenclatura or f"Parcela {self.pk}"

    class Meta:
        managed = False
        db_table = '"catastro"."parcela"'
        db_table_comment = 'Representa la parcela (vivienda) donde se realiza una intervención. Contiene datos del adjudicatario.'


class ResolucionCostos(models.Model):
    nro_largo = models.IntegerField(db_comment='Nro de Resolución')
    ano = models.IntegerField(db_comment='Año de la Resolución')
    tipo = models.TextField(db_comment='Tipo de Resolución de Costos (Definitiva, Provisoria)')  # This field type is a guess.
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nro_corto = models.IntegerField()

    def __str__(self):
        return f"Resolución {self.nro_corto}/{self.ano}"

    class Meta:
        managed = False
        db_table = '"catastro"."resolucion_costos"'
        db_table_comment = 'Representa una Resolución de Costos,  Definitiva o Provisoria'


class TipoContratacion(models.Model):
    nombre = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"catastro"."tipo_contratacion"'
        db_table_comment = 'Tipología de Contrataciones (Lic. Pub., Lic. Priv, Conc. Precios, Adj. Directa, etc.)'


class TipoEstado(models.Model):
    nombre = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"catastro"."tipo_estado"'
        db_table_comment = 'Tipos de Estado de uina intervención (en obra, paralizada, finalizada, cancelada)'


class TipoIntervencion(models.Model):
    nombre = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"catastro"."tipo_intervencion"'
        db_table_comment = 'Tipología de Intervención (Barrio, Vivienda, Mejora, Infraestructura, etc)'


class TipoUf(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = '"catastro"."tipo_uf"'


class ViviendasParaEscriturar(models.Model):
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
    ejecutores = models.TextField(blank=True, null=True)
    planos = models.TextField(blank=True, null=True)
    adjugisnroadju = models.IntegerField(db_column='AdjuGISNroAdju', blank=True, null=True)  # Field name made lowercase.
    adjugisescritura = models.CharField(db_column='AdjuGISEscritura', max_length=2, blank=True, null=True)  # Field name made lowercase.
    adjugisresacta = models.CharField(db_column='AdjuGISResActa', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugisresfecha = models.DateField(db_column='AdjuGISResFecha', blank=True, null=True)  # Field name made lowercase.
    adjugisresnro = models.IntegerField(db_column='AdjuGISResNro', blank=True, null=True)  # Field name made lowercase.
    adjugisapeynom = models.CharField(db_column='AdjuGISapeynom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugisdireccion = models.CharField(db_column='AdjuGISdireccion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugisdni = models.IntegerField(db_column='AdjuGISdni', blank=True, null=True)  # Field name made lowercase.
    adjugismatricula = models.CharField(db_column='AdjuGISmatricula', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugismotivo = models.CharField(db_column='AdjuGISmotivo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adjugissituacion = models.CharField(db_column='AdjuGISsituacion', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.uf or f"Vivienda para escriturar {self.pk}"

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = '"vistas"."viviendas_para_escriturar"'
        db_table_comment = 'WHERE a."AdjuGISEscritura"::text = \'NO\'::text /*AND a."AdjuGISResNro" > 0 AND v.planos <> \'\'::text*/;'
        permissions = [("ver_escriturar", "Puede ver la capa de Viviendas para Escriturar")]

