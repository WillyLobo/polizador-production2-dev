from datetime import datetime
from django.utils import timezone
from wsgiref.validate import validator
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.db.models import Sum, F, FloatField
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid_utils import compat
import os
from secretariador.functions import FileValidator, CuitValidator


# from .models import User

def generate_name_certificados(instance, filename):
    directorio = "certificados/"
    anio = str(instance.certificado_fecha.year)
    mes = str(instance.certificado_fecha.month)
    mes = mes.zfill(2)
    extension = "pdf"
    filename = f"{instance.certificado_uuid}_{instance.certificado_expediente}.{extension}"
    name = os.path.join(directorio, anio, mes, filename)
    return name

def generate_name_polizas(instance, filename):
    directorio = "polizas/"
    anio = str(instance.poliza_fecha.year)
    mes = str(instance.poliza_fecha.month)
    mes = mes.zfill(2)
    extension = "pdf"
    filename = f"{instance.poliza_uuid}_{instance.poliza_expediente}.{extension}"
    name = os.path.join(directorio, anio, mes, filename)
    return name

def generate_name_contratos(instance, filename):
    directorio = "contratos_obra/"
    extension = "pdf"
    filename = f"{instance.contratodigital_uuid}.{extension}"
    name = os.path.join(directorio, filename)
    return name

def generate_name_resoluciones(instance, filename):
    directorio = "resoluciones_obra/"
    extension = "pdf"
    filename = f"{instance.resoluciondigital_uuid}.{extension}"
    name = os.path.join(directorio, filename)
    return name

class Receptor(models.Model):
    class Meta:
        verbose_name = "Receptor"
        verbose_name_plural = "Receptores"
        ordering = ["receptor_nombre"]
    
    receptor_nombre = models.CharField("Receptor", max_length=100)
    receptor_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    receptor_history = HistoricalRecords()

    def __str__(self):
        return self.receptor_nombre
    
    def get_absolute_url(self):
        return reverse('update-receptor', kwargs={'id': self.pk})

class Area(models.Model):
    class Meta:
        verbose_name  = "Area"
        verbose_name_plural = "Areas"
        ordering = ["area_nombre"]
    
    area_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    area_nombre = models.CharField("Area", max_length=50)
    area_history = HistoricalRecords()

    def __str__(self):
        return self.area_nombre
    
    def get_absoute_url(self):
        return reverse('update-area', kwargs={'id': self.pk})

class Aseguradora(models.Model):
    class Meta:
        verbose_name = "Aseguradora"
        verbose_name_plural = "Aseguradoras"
        ordering = ["aseguradora_nombre"]
    
    aseguradora_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    aseguradora_nombre = models.CharField("Nombre Compañía Aseguradora", max_length=255)
    aseguradora_history = HistoricalRecords()

    def __str__(self):
        return self.aseguradora_nombre
    
    def get_absolute_url(self):
        return reverse('update-aseguradora', kwargs={'id': self.pk})

class Empresa(models.Model):
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["empresa_nombre"]
    
    empresa_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    empresa_nombre          = models.CharField("Nombre Empresa", max_length=255)
    empresa_cuit            = models.CharField("CUIT", max_length=11, blank=True, null=True)
    empresa_titular_titulo  = models.CharField("Titulo Representante", max_length=40, blank=True, null=True)
    empresa_titular_nombre  = models.CharField("Titular de la Empresa", max_length=140, blank=True, null=True)
    empresa_titular_dni     = models.DecimalField("DNI", max_digits=9, decimal_places=0, blank=True, null=True)
    empresa_direccion       = models.CharField("Dirección de la Empresa", max_length=255, blank=True, null=True)
    empresa_inscripcion     = models.CharField("Inscripción", max_length=500, blank=True, null=True)
    empresa_correo_p        = models.EmailField("Dirección de Correo Primaria", blank=True, null=True)
    empresa_correo_s        = models.EmailField("Dirección de Correo Alternativa", blank=True, null=True)
    empresa_history = HistoricalRecords()


    def __str__(self):
        return self.empresa_nombre
    
    def get_absolute_url(self):
        return reverse('update-empresa', kwargs={'id': self.pk})

class Poliza(models.Model):
    CONCEPTO = (
        ("C", "Garantía de Ejecución de Contrato"),
        ("F", "Garantía de Sustitución de Fondo de Reparo"),
        ("A", "Garantía de Anticipo Financiero")
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=["poliza_fecha", "poliza_numero", "poliza_aseguradora","poliza_tomador"], name="poliza-constraint")]
        verbose_name = "Póliza"
        verbose_name_plural = "Pólizas"
        ordering = ["poliza_fecha"]
    
    poliza_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    poliza_fecha = models.DateField("Fecha")
    poliza_expediente = models.CharField("Expediente", max_length=18)
    poliza_numero = models.IntegerField("Número de Póliza")
    poliza_concepto = models.CharField("Concepto", max_length=1, choices=CONCEPTO)
    poliza_anexo = models.CharField("Anexo de Póliza", max_length=40, blank=True, null=True)
    poliza_recibo = models.CharField("Número de Recibo", max_length=100)
    poliza_aseguradora = models.ForeignKey("Aseguradora", verbose_name="Aseguradora", on_delete=models.CASCADE)
    poliza_tomador = models.ForeignKey("Empresa", verbose_name="Tomador", on_delete=models.CASCADE)
    poliza_obra = models.ForeignKey("Obra", verbose_name="Obra", on_delete=models.CASCADE)
    poliza_monto_pesos = models.DecimalField("Monto Sustituido en Pesos", max_digits=15, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    poliza_monto_uvi = models.DecimalField("Monto Sustituido en UVI", max_digits=15, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    poliza_digital = models.FileField(verbose_name="Póliza Digital", upload_to=generate_name_polizas, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], max_length=500, null=True, blank=True)
    poliza_history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.poliza_numero} - {self.poliza_aseguradora.aseguradora_nombre} - {self.poliza_obra.obra_nombre} - {self.poliza_tomador.empresa_nombre} "

    def get_absolute_url(self):
        return reverse('estado-poliza', kwargs={'id': self.pk})

class Poliza_Movimiento(models.Model):
    class Meta:
        verbose_name = "Poliza_Movimiento"
        verbose_name_plural = "Polizas_Movimiento"
        ordering = ["poliza_movimiento_fecha"]
    
    poliza_movimiento_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    poliza_movimiento_fecha     = models.DateField("Fecha")
    poliza_movimiento_receptor  = models.ForeignKey("Receptor", verbose_name="Receptor", on_delete=models.CASCADE)
    poliza_movimiento_area      = models.ForeignKey("Area", verbose_name="Area", on_delete=models.CASCADE)
    poliza_movimiento_numero    = models.ForeignKey("Poliza", verbose_name="Póliza", on_delete=models.CASCADE)
    poliza_movimiento_history = HistoricalRecords()

    def __str__(self):
        return f"{self.poliza_movimiento_numero} - {self.poliza_movimiento_area} - ({self.poliza_movimiento_fecha})"
    
    def get_absolute_url(self):
        return reverse('estado-poliza', kwargs={'id': self.poliza_movimiento_numero.pk})

class Programa(models.Model):
    class Meta:
        verbose_name = "Programa"
        verbose_name_plural = "Programas"
        ordering = ["programa_nombre"]
    
    programa_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    programa_nombre = models.CharField(verbose_name="Nombre", max_length=255)
    programa_history = HistoricalRecords()

    def __str__(self):
        return self.programa_nombre
    
    def get_absolute_url(self):
        return reverse('update-programa', kwargs={'id': self.pk})

class Provincia(models.Model):
    class Meta:
        ordering = ["provincia_nombre"]
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
    
    provincia_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    id = models.IntegerField(unique=True, primary_key=True)
    provincia_nombre = models.CharField("Nombre Provincia", max_length=33)
    provincia_history = HistoricalRecords()

    def __str__(self):
        return f"{self.provincia_nombre}"

class Region(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Region"
    
    region_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    region_numero   = models.CharField("Número Región", max_length=10)
    region_history = HistoricalRecords()

    def __str__(self):
        return self.region_numero
    
    def get_absolute_url(self):
        return reverse('update-region', kwargs={'id': self.pk})


class Departamento(models.Model):
    class Meta:
        ordering			= ["departamento_nombre"]
        verbose_name_plural = "Departamentos"

    departamento_uuid		= models.UUIDField(default=compat.uuid7, editable=False)
    id					= models.IntegerField(unique=True, primary_key=True)
    departamento_nombre = models.TextField("Nombre Departamento")
    departamento_history = HistoricalRecords()

    def __str__(self):
        return self.departamento_nombre

    def get_abolute_url(self):
        return reverse('update-departamento', kwargs={'id': self.pk})

class Localidad(models.Model):
    class Meta:
        ordering			= ["localidad_nombre"]
        verbose_name_plural = "Localidades"

    localidad_uuid		= models.UUIDField(default=compat.uuid7, editable=False)
    localidad_nombre		= models.TextField("Nombre Localidad")
    id                      = models.IntegerField("Id", unique=True, primary_key=True) 
    localidad_centroide_lat	= models.DecimalField("Latitud Centroide", max_digits=15, decimal_places=13,blank=True, null=True)
    localidad_centroide_lon	= models.DecimalField("Longitud Centroide", max_digits=15, decimal_places=13,blank=True, null=True)
    localidad_funcion       = models.CharField("Función",max_length=40,blank=True, null=True)
    localidad_departamento	= models.ForeignKey("Departamento", verbose_name="Departamento", on_delete=models.RESTRICT)
    localidad_municipio     = models.ForeignKey("Municipio", verbose_name="Municipio", on_delete=models.CASCADE)
    localidad_history = HistoricalRecords()

    def __str__(self):
        return self.localidad_nombre
    # return "{} - Departamento {}".format(self.localidad_nombre, self.localidad_departamento)

    def get_absolute_url(self):
        return reverse('update-localidad', kwargs={'id': self.pk})

class Municipio(models.Model):
    class Meta:
        ordering 			= ["municipio_nombre"]
        verbose_name_plural = "Municipios"

    municipio_uuid        = models.UUIDField(default=compat.uuid7, editable=False)
    municipio_nombre        = models.CharField("Nombre",max_length=40)
    id                      = models.IntegerField("Id", unique=True, primary_key=True)
    municipio_departamento  = models.ForeignKey("Departamento", verbose_name="Departamento", on_delete=models.CASCADE)
    municipio_region        = models.ForeignKey("Region", verbose_name="Región", on_delete=models.DO_NOTHING, null=True, blank=True)
    municipio_history = HistoricalRecords()

    def __str__(self):
        return self.municipio_nombre
    
    def get_absolute_url(self):
        return reverse('update-municipio', kwargs={'id': self.pk})

class Obra(models.Model):
    COMPULSA = (
        ("L", "Licitación Pública"),
        ("P", "Licitación Privada"),
        ("C", "Concurso de Precios"),
        ("D", "Contratación Directa")
    )
    
    class Meta:
        # constraints = [models.UniqueConstraint(fields=["obra_nombre", "obra_empresa", "obra_convenio","obra_programa"], name="obra-constraint")]
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        ordering = ["obra_programa", "obra_convenio", "obra_nombre"]

    obra_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    obra_nombre = models.TextField("Nombre", help_text="Nombre de la Obra tal como figura en el contrato")
    obra_soluciones = models.DecimalField("Cantidad de soluciones", max_digits=4, decimal_places=0, null=True, blank=True)
    obra_empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, verbose_name="Empresa")
    obra_region = models.ForeignKey("Region", on_delete=models.CASCADE, verbose_name="Región", null=True, blank=True)
    obra_departamento_m = models.ManyToManyField("Departamento", related_name="obra_departamento", verbose_name="Departamento", blank=True)
    obra_municipio_m = models.ManyToManyField("Municipio", related_name="obra_municipio", verbose_name="Municipio", blank=True)
    obra_localidad_m = models.ManyToManyField("Localidad", related_name="obra_localidad", verbose_name="Localidad", blank=True)
    obra_conjunto = models.ForeignKey("ConjuntoLicitado", verbose_name="Conjunto Licitado", on_delete=models.DO_NOTHING, null=True, blank=True)
    obra_grupo = models.CharField("Grupo", max_length=4, blank=True, null=True)
    obra_plazo = models.CharField("Plazo de Ejecución", max_length=10, blank=True, null=True)
    obra_programa = models.ForeignKey("Programa", verbose_name="Programa", on_delete=models.CASCADE)
    obra_convenio = models.CharField("Convenio/ACU", max_length=60, blank=True, null=True)
    obra_expediente = models.CharField("Expediente", max_length=18)
    obra_resolucion = models.CharField("Resolución de Adjudicación", max_length=15, blank=True, null=True)
    obra_licitacion_tipo = models.CharField("Compulsa", max_length=1, choices=COMPULSA, blank=True, null=True)
    obra_licitacion_numero = models.DecimalField("Número de Licitación", max_digits=3, decimal_places=0, blank=True, null=True)
    obra_licitacion_ano = models.DecimalField("Año de Licitación", max_digits=4, decimal_places=0, blank=True, null=True)
    obra_nomenclatura = models.CharField("Nomenclatura Catastral", max_length=1000, blank=True, null=True)  
    obra_nomenclatura_plano = models.CharField("Número de Plano", max_length=10, blank=True, null=True)
    obra_fecha_entrega = models.DateField("Fecha de Entrega de la Obra", blank=True, null=True)
    obra_fecha_contrato = models.DateField("Fecha de Firma de Contrato", blank=True, null=True)
    obra_expediente_costo = models.CharField("Expediente de Costos", max_length=18, blank=True, null=True)
    obra_inspector = models.ManyToManyField("personalizador.Agente", related_name="obra_inspector", verbose_name="Inspector")
    obra_observaciones = models.TextField("Observaciones", blank=True, null=True)
    obra_contrato_nacion_pesos = models.DecimalField("Monto Nación en Pesos", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_nacion_uvi = models.DecimalField("Monto Nación en UVI", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_nacion_uvi_fecha = models.DateField("Fecha UVI Nación", blank=True, null=True)
    obra_contrato_provincia_pesos = models.DecimalField("Monto Provincia en Pesos", max_digits=12 ,decimal_places=2, default=0 , validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_provincia_uvi = models.DecimalField("Monto Provincia en UVI", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_provincia_uvi_fecha = models.DateField("Fecha UVI Provicia", blank=True, null=True)
    obra_contrato_terceros_pesos = models.DecimalField("Monto Terceros en Pesos", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_terceros_uvi = models.DecimalField("Monto Terceros en UVI", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_terceros_uvi_fecha = models.DateField("Fecha UVI Terceros", blank=True, null=True)
    obra_contrato_total_pesos = models.GeneratedField(
        expression=F("obra_contrato_nacion_pesos") + F("obra_contrato_terceros_pesos") + F("obra_contrato_provincia_pesos"),
        output_field=models.DecimalField(max_digits=12, decimal_places=2, editable=False),
        db_persist=True,
    )
    obra_contrato_total_uvi             = models.GeneratedField(
        expression=F("obra_contrato_nacion_uvi") + F("obra_contrato_terceros_uvi") + F("obra_contrato_provincia_uvi"),
        output_field=models.DecimalField(max_digits=12, decimal_places=2, editable=False),
        db_persist=True,
    )
    obra_principal = models.ManyToManyField("Obra", related_name="obra_madre", verbose_name="Obra Madre", blank=True)
    obra_history = HistoricalRecords(excluded_fields=['obra_contrato_total_pesos', "obra_contrato_total_uvi"])
        
    def obra_acum_pesos(self):
        if self.certificado_set:
            return self.certificado_set.aggregate(Sum(F("certificado_monto_cobrar"), output_field=FloatField()))
        else:
            return 0
        
    def obra_acum_uvi(self):
        if self.certificado_set:
            return self.certificado_set.aggregate(Sum(F("certificado_monto_cobrar_uvi"), output_field=FloatField()))
        else:
            return 0
    
    def saldo_uvi(self):
        try:
            if self.certificado_set:
                agregado = self.certificado_set.aggregate(Sum(F("certificado_monto_cobrar_uvi")))["certificado_monto_cobrar_uvi__sum"]
                contrato = self.obra_contrato_total_uvi
                saldo = contrato - agregado
                return saldo
            else:
                return self.obra_contrato_total_uvi
        except TypeError:
            return 0
    
    def obra_acum_pct(self):
        if self.certificado_set:
            return self.certificado_set.latest().certificado_acum_pct

    def plan_vigente(self):
        """Retorna el Plan de Trabajos más reciente (vigente) de la obra."""
        return self.plandetrabajos_set.order_by("-trabajos_fecha", "-pk").first()

    def clean(self):
        self.obra_contrato_nacion_pesos = 0 if self.obra_contrato_nacion_pesos is None else self.obra_contrato_nacion_pesos
        self.obra_contrato_nacion_uvi = 0 if self.obra_contrato_nacion_uvi is None else self.obra_contrato_nacion_uvi
        self.obra_contrato_nacion_uvi_fecha = 0 if self.obra_contrato_nacion_uvi_fecha is None else self.obra_contrato_nacion_uvi_fecha
        self.obra_contrato_provincia_pesos = 0 if self.obra_contrato_provincia_pesos is None else self.obra_contrato_provincia_pesos
        self.obra_contrato_provincia_uvi = 0 if self.obra_contrato_provincia_uvi is None else self.obra_contrato_provincia_uvi
        self.obra_contrato_provincia_uvi_fecha = 0 if self.obra_contrato_provincia_uvi_fecha is None else self.obra_contrato_provincia_uvi_fecha
        self.obra_contrato_terceros_pesos = 0 if self.obra_contrato_terceros_pesos is None else self.obra_contrato_terceros_pesos
        self.obra_contrato_terceros_uvi = 0 if self.obra_contrato_terceros_uvi is None else self.obra_contrato_terceros_uvi
        self.obra_contrato_terceros_uvi_fecha = 0 if self.obra_contrato_terceros_uvi_fecha is None else self.obra_contrato_terceros_uvi_fecha
    
    def __str__(self):
        return f"({self.obra_convenio if self.obra_convenio else ''}) {self.obra_nombre} - {self.obra_empresa}"
    
    def lista_localidades(self):
        return ", ".join(str(localidad) for localidad in self.obra_localidad_m.all())
    
    def get_absolute_url(self):
        return reverse('estado-obra', kwargs={'id': self.pk})

class Prototipo(models.Model):
    TIPO = (
        ("1", "1 Dormitorio"),
        ("2", "2 Dormitorios"),
        ("3", "3 Dormitorios"),
        ("4", "4 Dormitorios"),
        ("o", "Otro")
    )

    class Meta:
        verbose_name = "Prototipo Habitacional"
        verbose_name_plural = "Prototipos Habitacionales"
    
    prototipo_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    prototipo_obra = models.ForeignKey("Obra", verbose_name="Obra", on_delete=models.DO_NOTHING)
    prototipo_tipo = models.CharField("Tipo de Prototipo", max_length=1, choices=TIPO)
    prototipo_cantidad = models.DecimalField("Cantidad del Prototipo", max_digits=3, decimal_places=0)
    prototipo_superficie = models.DecimalField("Superficie del Prototipo", max_digits=3, decimal_places=0)
    prototipo_uvi = models.DecimalField("UVIs x M2", max_digits=5, decimal_places=2)
    prototipo_incremento = models.DecimalField("Incremento Porcentual por Infraestructura", max_digits=2, decimal_places=0)
    prototipo_discapacitado = models.BooleanField("Es Prototipo para Discapacitado", default=False)
    prototipo_history = HistoricalRecords()

class CertificadoRubro(models.Model):
    class Meta:
        verbose_name_plural = "Rubros"
        ordering = ["certificadorubro_nombre"]
    
    certificadorubro_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    certificadorubro_nombre = models.CharField("Rubro", max_length=100)
    certificadorubro_nombre_corto = models.CharField("Rubro Corto", max_length=1)
    certificadorubro_history = HistoricalRecords()

    def __str__(self):
        return f"{self.certificadorubro_nombre}"

class CertificadoFinanciamiento(models.Model):
    class Meta:
        verbose_name_plural = "Financiamiento"
        ordering = ["certificadofinanciamiento_nombre"]
    
    certificadofinanciamiento_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    certificadofinanciamiento_nombre = models.CharField("Financiamiento", max_length=100)
    certificadofinanciamiento_nombre_corto = models.CharField("Financiamiento Corto", max_length=1)
    certificadofinanciamiento_history = HistoricalRecords()

    def __str__(self):
        return f"{self.certificadofinanciamiento_nombre}"
    
class Certificado(models.Model):
    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        get_latest_by = "certificado_fecha"
        ordering = ["certificado_fecha", "certificado_expediente"]
    FINANCIAMIENTO = (
        ("N", "Nación"),
        ("P", "Provincia"),
        ("T", "Terceros")
    )
    # Obsoleto -> se migro a una tabla aparte(carga.models.CertificadoRubro)
    RUBRO = (
        ("V", "Vivienda"),
        ("F", "Infraestructura Frentista"),
        ("T", "Terreno"),
        ("R", "Redeterminación"),
        ("I", "Nexos y Redes"),
        ("C", "Complementario"),
        ("M", "Deductivo")
    )

    certificado_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    certificado_obra = models.ForeignKey("Obra", verbose_name="Obra", on_delete=models.CASCADE)
    certificado_financiamiento = models.CharField("Financiamiento", max_length=1, choices=FINANCIAMIENTO, default="N")
    certificado_rubro = models.CharField("Rubro", max_length=1, choices=RUBRO, default="V") # Obsoleto -> se migro a una tabla aparte(carga.models.CertificadoRubro)
    certificado_rubro_db = models.ForeignKey("CertificadoRubro", verbose_name="Rubro", on_delete=models.DO_NOTHING, default=1)
    certificado_rubro_anticipo = models.DecimalField("Anticipo N°", max_digits=3, decimal_places=0, blank=True, default=0, validators=[MinValueValidator(0)])
    certificado_rubro_obra = models.DecimalField("Obra N°", max_digits=3, decimal_places=0, blank=True, default=0, validators=[MinValueValidator(0)])
    certificado_rubro_devanticipo = models.DecimalField("Devolución de Anticipo N°", max_digits=3, decimal_places=0, blank=True, default=0, validators=[MinValueValidator(0)])
    certificado_expediente = models.CharField("Número de Expediente", max_length=18)
    certificado_periodo = models.CharField("Periodo", max_length=13, null=True, blank=True)
    certificado_monto_pesos = models.DecimalField("Monto en Pesos", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    certificado_mes_pct = models.DecimalField("Mes %", max_digits=5, decimal_places=2, default=0, validators=[MaxValueValidator(100)])
    certificado_ante_pct = models.DecimalField("Anterior %", max_digits=5, decimal_places=2, default=0, validators=[MaxValueValidator(100)])
    certificado_acum_pct = models.DecimalField("Acumulado %", max_digits=5, decimal_places=2, default=0, validators=[MaxValueValidator(100)])
    certificado_devolucion_expte = models.CharField("Número de Expediente Devolución", max_length=18, null=True, blank=True)
    certificado_devolucion_monto = models.DecimalField("Monto Devolución en Pesos", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    certificado_devolucion_monto_uvi = models.DecimalField("Monto Devolución en UVI", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    certificado_monto_uvi = models.DecimalField("Monto en UVI", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    certificado_fecha = models.DateField("Fecha", default=timezone.now)
    certificado_monto_cobrar = models.GeneratedField(
        expression=F("certificado_monto_pesos") - F("certificado_devolucion_monto"),
        output_field=models.DecimalField("Monto a Cobrar Pesos", max_digits=12, decimal_places=2, default=0, editable=False),
        db_persist=True
    )
    certificado_monto_cobrar_uvi = models.GeneratedField(
        expression=F("certificado_monto_uvi") - F("certificado_devolucion_monto_uvi"),
        output_field=models.DecimalField("Monto a Cobrar UVI", max_digits=12, decimal_places=2, default=0, editable=False),
        db_persist=True
    )
    certificado_digital = models.FileField(upload_to=generate_name_certificados, max_length=500, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
    certificado_fecha_carga = models.DateField("Fecha de carga", default=timezone.now)
    certificado_fecha_carga_legacy = models.BooleanField("Es Certificado Viejo", default=False)
    certificado_foja = models.ForeignKey("FojaDeMedicion", verbose_name="Foja de Medición de Origen", on_delete=models.SET_NULL, null=True, blank=True)
    certificado_history = HistoricalRecords(excluded_fields=['certificado_monto_cobrar', "certificado_monto_cobrar_uvi"])
    
    def clean(self):
        self.certificado_rubro_anticipo = 0 if self.certificado_rubro_anticipo else self.certificado_rubro_anticipo
        self.certificado_rubro_obra = 0 if self.certificado_rubro_obra else self.certificado_rubro_obra
        self.certificado_rubro_devanticipo = 0 if self.certificado_rubro_devanticipo else self.certificado_rubro_devanticipo
        self.certificado_monto_pesos = 0 if self.certificado_monto_pesos else self.certificado_monto_pesos
        self.certificado_devolucion_monto = 0 if self.certificado_devolucion_monto else self.certificado_devolucion_monto
        self.certificado_devolucion_monto_uvi = 0 if self.certificado_devolucion_monto_uvi else self.certificado_devolucion_monto_uvi
        self.certificado_monto_uvi = 0 if self.certificado_monto_uvi else self.certificado_monto_uvi

    def __str__(self):
        return f"{self.certificado_obra} - {self.certificado_expediente} - Rubro: {self.get_certificado_rubro_display()} - Financiamiento: {self.get_certificado_financiamiento_display()} - Ant. N°{self.certificado_rubro_anticipo} - Ob. N°{self.certificado_rubro_obra} - Dev. N°{self.certificado_rubro_devanticipo}"
    
    def get_absolute_url(self):
        return reverse('update-certificado', kwargs={'id': self.pk})

class ConjuntoLicitado(models.Model):
    class Meta:
        ordering = ["id", "conjunto_nombre"]
        verbose_name_plural = "Conjuntos Licitados"

    conjunto_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    conjunto_nombre = models.TextField("Nombre")
    conjunto_soluciones = models.DecimalField("Cantidad de Soluciones", max_digits=5, decimal_places=0, default=0, null=True, blank=True)
    conjunto_resolucion = models.CharField("Resolucion", max_length=15, null=True, blank=True)
    conjunto_subconjunto = models.ForeignKey("ConjuntoLicitado", verbose_name="Conjunto Licitado", on_delete=models.DO_NOTHING, null=True, blank=True)
    conjunto_history = HistoricalRecords()

    def __str__(self):
        return f"{self.conjunto_nombre}"
    
    def get_absolute_url(self):
        return reverse('update-conjunto', kwargs={'id': self.pk})

class PlanDeTrabajos(models.Model):
    class Meta:
        verbose_name_plural = "Plan de Trabajos"

    trabajos_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    trabajos_obra = models.ForeignKey("Obra", on_delete=models.DO_NOTHING)
    trabajos_fecha = models.DateField("Fecha de Vigencia", default=timezone.now)
    trabajos_history = HistoricalRecords()

    @classmethod
    def vigentes(cls):
        """Devuelve el queryset con el plan vigente (más reciente) de cada obra."""
        from django.db.models import OuterRef, Subquery
        ultimo = cls.objects.filter(trabajos_obra=OuterRef("trabajos_obra")).order_by("-trabajos_fecha", "-pk")
        return cls.objects.filter(pk=Subquery(ultimo.values("pk")[:1]))

    def es_vigente(self):
        return PlanDeTrabajos.vigentes().filter(pk=self.pk).exists()

    def __str__(self):
        return f"Plan de Trabajos - {self.trabajos_obra}"

    def get_absolute_url(self):
        return reverse('carga:update-plandetrabajos', kwargs={'pk': self.pk})

class PlanDeTrabajosRubro(models.Model):
    class Meta:
        verbose_name = "Rubro de Plan de Trabajos"
        verbose_name_plural = "Rubros de Plan de Trabajos"
        ordering = ["rubro_plan", "rubro_orden"]

    rubro_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    rubro_plan = models.ForeignKey("PlanDeTrabajos", verbose_name="Plan de Trabajos", on_delete=models.CASCADE, related_name="rubros")
    rubro_nombre = models.CharField("Rubro", max_length=200)
    rubro_orden = models.PositiveIntegerField("Orden", default=0)
    rubro_presupuesto = models.DecimalField("Presupuesto", max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    rubro_anterior = models.ForeignKey("self", verbose_name="Rubro Anterior (Plan Previo)", on_delete=models.SET_NULL, null=True, blank=True, related_name="rubro_siguiente")
    rubro_history = HistoricalRecords()

    def rubro_cadena_ids(self):
        """IDs de este rubro y todos sus predecesores (reprogramaciones anteriores)."""
        ids = [self.pk]
        actual = self
        while actual.rubro_anterior_id:
            actual = actual.rubro_anterior
            ids.append(actual.pk)
        return ids

    def __str__(self):
        return f"{self.rubro_nombre} - {self.rubro_plan}"

    def get_absolute_url(self):
        return reverse('carga:update-plandetrabajosrubro', kwargs={'pk': self.pk})

class PlanDeTrabajosItem(models.Model):
    class Meta:
        verbose_name = "Item de Plan de Trabajos"
        verbose_name_plural = "Items de Plan de Trabajos"
        ordering = ["planitem_rubro", "planitem_orden"]

    planitem_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    planitem_rubro = models.ForeignKey("PlanDeTrabajosRubro", verbose_name="Rubro de Plan de Trabajos", on_delete=models.CASCADE, related_name="items")
    planitem_nombre = models.CharField("Item", max_length=200)
    planitem_orden = models.PositiveIntegerField("Orden", default=0)
    planitem_incidencia_pct = models.DecimalField("Incidencia %", max_digits=6, decimal_places=3, validators=[MinValueValidator(0), MaxValueValidator(100)])
    item_anterior = models.ForeignKey("self", verbose_name="Item Anterior (Plan Previo)", on_delete=models.SET_NULL, null=True, blank=True, related_name="item_siguiente")
    planitem_history = HistoricalRecords()

    def item_cadena_ids(self):
        """IDs de este item y todos sus predecesores (reprogramaciones anteriores)."""
        ids = [self.pk]
        actual = self
        while actual.item_anterior_id:
            actual = actual.item_anterior
            ids.append(actual.pk)
        return ids

    def __str__(self):
        return f"{self.planitem_nombre} ({self.planitem_incidencia_pct}%) - {self.planitem_rubro}"

class FojaDeMedicion(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["foja_rubro", "foja_numero"], name="foja-numero-unico")
        ]
        verbose_name = "Foja de Medición"
        verbose_name_plural = "Fojas de Medición"
        ordering = ["foja_rubro", "foja_numero"]

    foja_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    foja_rubro = models.ForeignKey("PlanDeTrabajosRubro", verbose_name="Rubro de Plan de Trabajos", on_delete=models.CASCADE, related_name="fojas")
    foja_numero = models.PositiveIntegerField("Número de Foja", editable=False, default=1)
    foja_periodo = models.DateField("Período (Mes)")
    foja_fecha = models.DateField("Fecha de Medición", default=timezone.now)
    foja_inspector = models.ManyToManyField("personalizador.Agente", related_name="foja_inspector", verbose_name="Inspector", blank=True)
    foja_observaciones = models.TextField("Observaciones", blank=True, null=True)
    foja_history = HistoricalRecords()

    def foja_pct_avance_mes(self):
        total = 0
        for item in self.items.all():
            total += item.fojaitem_pct_avance_mes
        return total

    def foja_pct_acumulado(self):
        total = 0
        for item in self.items.all():
            total += item.fojaitem_pct_acumulado
        return total

    def foja_anterior(self):
        """Retorna la foja anterior, considerando también rubros de planes reprogramados."""
        chain_ids = self.foja_rubro.rubro_cadena_ids()
        return FojaDeMedicion.objects.filter(
            foja_rubro_id__in=chain_ids, foja_numero__lt=self.foja_numero
        ).order_by('-foja_numero').first()

    @staticmethod
    def anterior_items_map(rubro, items=None, exclude_foja_numero=None):
        """Acumulado %% de cada item en la foja anterior (misma lógica que FojaDeMedicionItem.save()).

        La foja anterior se determina por número de foja dentro de la cadena de rubros
        reprogramados, no por período: el período es solo una etiqueta y el número de
        foja se asigna por orden de creación (ver signals.auto_increment_foja_numero).
        """
        chain_ids = rubro.rubro_cadena_ids()
        qs = FojaDeMedicion.objects.filter(foja_rubro_id__in=chain_ids)
        if exclude_foja_numero is not None:
            qs = qs.filter(foja_numero__lt=exclude_foja_numero)
        foja_anterior = qs.order_by('-foja_numero').first()
        if not foja_anterior:
            return {}

        if items is None:
            items = PlanDeTrabajosItem.objects.filter(planitem_rubro=rubro)

        anterior_map = {}
        for item in items:
            previous_item = foja_anterior.items.filter(
                fojaitem_planitem_id__in=item.item_cadena_ids()
            ).first()
            if previous_item:
                anterior_map[item.pk] = previous_item.fojaitem_pct_acumulado
        return anterior_map

    def __str__(self):
        return f"Foja {self.foja_numero} - {self.foja_rubro}"

    def get_absolute_url(self):
        return reverse('carga:update-fojademedicion', kwargs={'pk': self.pk})

class FojaDeMedicionItem(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=["fojaitem_foja", "fojaitem_planitem"], name="fojaitem-planitem-unico")]
        verbose_name = "Item de Foja de Medición"
        verbose_name_plural = "Items de Foja de Medición"
        ordering = ["fojaitem_planitem__planitem_orden"]

    fojaitem_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    fojaitem_foja = models.ForeignKey("FojaDeMedicion", verbose_name="Foja de Medición", on_delete=models.CASCADE, related_name="items")
    fojaitem_planitem = models.ForeignKey("PlanDeTrabajosItem", verbose_name="Item del Plan", on_delete=models.CASCADE)
    fojaitem_pct_avance_mes = models.DecimalField("Avance del Mes %", max_digits=6, decimal_places=3, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fojaitem_pct_acumulado = models.DecimalField("Acumulado %", max_digits=6, decimal_places=3, default=0, editable=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fojaitem_history = HistoricalRecords()

    def __str__(self):
        return f"{self.fojaitem_planitem.planitem_nombre} - {self.fojaitem_foja}"

    def save(self, *args, **kwargs):
        foja_anterior = self.fojaitem_foja.foja_anterior()

        previous_item = None
        if foja_anterior:
            item_chain_ids = self.fojaitem_planitem.item_cadena_ids()
            previous_item = FojaDeMedicionItem.objects.filter(
                fojaitem_foja=foja_anterior,
                fojaitem_planitem_id__in=item_chain_ids
            ).first()

        if previous_item:
            self.fojaitem_pct_acumulado = previous_item.fojaitem_pct_acumulado + self.fojaitem_pct_avance_mes
        else:
            self.fojaitem_pct_acumulado = self.fojaitem_pct_avance_mes

        super(FojaDeMedicionItem, self).save(*args, **kwargs)
class Contrato(models.Model):
    class Meta:
        verbose_name_plural = "Contratos"
        ordering = ["contrato_fecha"]

    contrato_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    contrato_obra = models.ForeignKey("Obra", verbose_name="Obra", on_delete=models.CASCADE)
    contrato_fecha = models.DateField("Fecha",default=timezone.now)
    contrato_descripcion = models.CharField("Descripción", max_length=600, default="")
    contrato_resolucion = models.CharField("Resolución Aprobatoria", max_length=15, blank=True, null=True)
    contrato_autocarga = models.BooleanField("Contrato importado de formato anterior", editable=False, default=False)
    contrato_decreto = models.CharField("Decreto Aprobatorio(Si Tuviera)", max_length=15, blank=True, null=True)
    contrato_history = HistoricalRecords()

    def __str__(self):
        return f"{self.contrato_descripcion} - {self.contrato_obra}"

class ContratoMonto(models.Model):
    class Meta:
        verbose_name_plural = "Montos de Contrato"
        ordering = ["contratomonto_contrato"]
    
    contratomonto_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    contratomonto_contrato = models.ForeignKey("Contrato", verbose_name="Contrato", on_delete=models.CASCADE)
    contratomonto_rubro = models.ForeignKey("CertificadoRubro", verbose_name="Rubro Certificado", on_delete=models.CASCADE)
    contratomonto_financiamiento = models.ForeignKey("CertificadoFinanciamiento", verbose_name="Financiamiento", on_delete=models.CASCADE)
    contratomonto_pesos = models.DecimalField("Monto Pesos", max_digits=15, decimal_places=2, default=0)
    contratomonto_uvi = models.DecimalField("Monto UVI", max_digits=15, decimal_places=2, default=0)
    contratomonto_uvi_fecha = models.DateField("Fecha UVI:", blank=True, null=True)
    contratomonto_history = HistoricalRecords()

    def __str__(self):
        return f"{self.contratomonto_rubro}({self.contratomonto_financiamiento}) - {self.contratomonto_contrato}"
    
class ContratoRubro(models.Model):
    class Meta:
        verbose_name_plural = "Rubros de Contrato"
        ordering = ["contratorubro_tipo"]
    
    contratorubro_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    contratorubro_tipo = models.CharField("Rubro:", max_length=100)
    contratorubro_history = HistoricalRecords()

    def __str__(self):
        return f"{self.contratorubro_tipo}"
    
class ContratosDigitales(models.Model):
    class Meta:
        verbose_name_plural = "Contratos Digitales"
        ordering = ["id"]
    
    contratodigital_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    contratodigital_obra = models.ManyToManyField("Obra", related_name="obra_contratos", verbose_name="Obras", blank=True)
    contratodigital_nombre_archivo = models.CharField("Nombre del Archivo", max_length=100, blank=True, null=True)
    contratodigital_descripcion = models.TextField("Descripción")
    contratodigital_tipo = models.ForeignKey("ContratoRubro", verbose_name="Rubro Contrato", on_delete=models.CASCADE)
    contratodigital_archivo = models.FileField(upload_to=generate_name_contratos, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], max_length=500, null=True, blank=True)
    contratodigital_history = HistoricalRecords()

class ResolucionesDigitales(models.Model):
    class Meta:
        verbose_name_plural = "Resoluciones Digitales"
        ordering = ["resoluciondigital_numero"]
    
    resoluciondigital_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    resoluciondigital_obra = models.ManyToManyField("Obra", related_name="obra_resoluciones", verbose_name="Obras", blank=True)
    resoluciondigital_descripcion = models.TextField("Descripción")
    resoluciondigital_numero = models.CharField("Resolución", max_length=15)
    resoluciondigital_archivo = models.FileField(upload_to=generate_name_resoluciones, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], max_length=500, null=True, blank=True)
    resoluciondigital_history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.resoluciondigital_numero}"

class Uvi(models.Model):
    class Meta:
        verbose_name_plural = "UVI"
        ordering = ["-uvi_fecha",]
        get_latest_by = "-uvi_fecha"

    uvi_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    uvi_fecha = models.DateField("Fecha UVI:")
    uvi_valor = models.DecimalField("Valor", max_digits=15, decimal_places=2)
    uvi_history = HistoricalRecords()

    def __str__(self):
        return f"({self.id})-{self.uvi_fecha} - {self.uvi_valor}"

class INDEC(models.Model):

    class Meta:
        verbose_name_plural = "INDEC"
        ordering = ["mes"]

    indec_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    mes = models.DateField("Fecha de Medición")
    indec_manodeobra = models.DecimalField("Mano de Obra", max_digits=20, decimal_places=10)
    indec_albanileria = models.DecimalField("Albañilería", max_digits=20, decimal_places=10)
    indec_carpinterías = models.DecimalField("Carpinterías", max_digits=20, decimal_places=10)
    indec_andamios = models.DecimalField("Andamios", max_digits=20, decimal_places=10)
    indec_iluminación = models.DecimalField("Artefactos de iluminación y cableado", max_digits=20, decimal_places=10)
    indec_pvc = models.DecimalField("Caños de PVC para instalaciones varias", max_digits=20, decimal_places=10)
    indec_gastos = models.DecimalField("Gastos Generales", max_digits=20, decimal_places=10)
    indec_artefactos = models.DecimalField("Artefactos para baño y grifería", max_digits=20, decimal_places=10)
    indec_hormigon = models.DecimalField("Hormigón", max_digits=20, decimal_places=10)
    indec_valvulas = models.DecimalField("Válvulas de bronce", max_digits=20, decimal_places=10)
    indec_electrobombas = models.DecimalField("Electrobombas", max_digits=20, decimal_places=10)
    indec_quimicos = models.DecimalField("Productos Químicos", max_digits=20, decimal_places=10)
    indec_motores = models.DecimalField("Motores eléctricos y equipos de aire acondicionado", max_digits=20, decimal_places=10)
    indec_asfaltos = models.DecimalField("Asfaltos, combustibles y lubricantes", max_digits=20, decimal_places=10)
    indec_medidores = models.DecimalField("Medidores de caudal", max_digits=20, decimal_places=10)
    indec_membrana = models.DecimalField("Membrana impermeabilizante", max_digits=20, decimal_places=10)
    indec_equipo = models.DecimalField("Equipo - Amortización de equipo", max_digits=20,decimal_places=10)
    indec_pisos = models.DecimalField("Pisos y revestimientos", max_digits=20, decimal_places=10)
    indec_aceros = models.DecimalField("Aceros - Hierro aletado", max_digits=20, decimal_places=10)
    indec_cemento = models.DecimalField("Cemento", max_digits=20, decimal_places=10)
    indec_arena = models.DecimalField("Arena", max_digits=20, decimal_places=10)
    indec_costo_financiero = models.DecimalField("Costo Financiero", max_digits=20, decimal_places=10, default=18.85)
    indec_transporte = models.DecimalField("Transporte", max_digits=20, decimal_places=10, default=134.98)
    indec_history = HistoricalRecords()

    def __str__(self):
        return f"{self.mes}"