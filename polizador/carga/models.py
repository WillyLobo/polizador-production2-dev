from datetime import datetime
from django.utils import timezone
from wsgiref.validate import validator
from django.db import models
from django.db.models import Sum, F, FloatField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User 
import os

# from .models import User

def generate_name(instance, filename):
    directorio = "certificados/"
    fecha = datetime.now().strftime("%m-%Y")
    extension = filename.split(".")[-1]
    filename = "{}.{}".format(instance, extension).replace("#","-").replace("/","-").replace("[","(").replace("]",")").replace("*","-").replace("?","-")
    name = os.path.join(directorio, fecha, filename)
    return name

def generate_name_poliza(instance, filename):
    directorio = "polizas/"
    fecha = datetime.now().strftime("%m-%Y")
    extension = filename.split(".")[-1]
    filename = "{} - {} - {}.{}".format(instance.poliza_numero, instance.poliza_aseguradora, instance.poliza_expediente, extension).replace("#","-").replace("/","-").replace("[","(").replace("]",")").replace("*","-").replace("?","-")
    name = os.path.join(directorio, fecha, filename)
    return name

def generate_name_contratos(instance, filename):
    file = filename.split("/")[-1]
    extension = file.split(".")[-1]
    filename = file.split(".")[0]
    directorio = "contratos/"
    filename = "{}.{}".format(filename, extension).replace("#","-").replace("/","-").replace("[","(").replace("]",")").replace("*","-").replace("?","-")
    name = os.path.join(directorio, filename)
    return name

def generate_name_resoluciones(instance, filename):
    file = filename.split("/")[-1]
    extension = file.split(".")[-1]
    filename = file.split(".")[0]
    directorio = "resoluciones/"
    filename = "{}.{}".format(filename, extension).replace("#","-").replace("/","-").replace("[","(").replace("]",")").replace("*","-").replace("?","-")
    name = os.path.join(directorio, filename)
    return name

class Receptor(models.Model):
    class Meta:
        verbose_name = "Receptor"
        verbose_name_plural = "Receptores"
    
    receptor_nombre = models.CharField("Receptor", max_length=100)

    def __str__(self):
        return self.receptor_nombre
    
    def get_absolute_url(self):
        return f"/polizas/crear/receptor/{self.id}"
    

class Area(models.Model):
    class Meta:
        verbose_name  = "Area"
        verbose_name_plural = "Areas"
    
    area_nombre = models.CharField("Area", max_length=50)

    def __str__(self):
        return self.area_nombre
    
    def get_absoute_url(self):
        return f"/polizas/crear/area/{self.id}"

class Aseguradora(models.Model):
    class Meta:
        verbose_name = "Aseguradora"
        verbose_name_plural = "Aseguradoras"
    
    aseguradora_nombre = models.CharField("Nombre Empresa Aseguradora", max_length=255)

    def __str__(self):
        return self.aseguradora_nombre
    
    def get_absolute_url(self):
        return f"/polizas/crear/aseguradora/{self.id}"

class Empresa(models.Model):
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
    
    empresa_nombre          = models.CharField("Nombre Empresa Tomadora:", max_length=255)
    empresa_cuit            = models.CharField("CUIT:", max_length=11, blank=True, null=True)
    empresa_titular_titulo  = models.CharField("Titulo Representante:", max_length=40, blank=True, null=True)
    empresa_titular_nombre  = models.CharField("Titular de la Empresa", max_length=140, blank=True, null=True)
    empresa_titular_dni     = models.DecimalField("DNI:", max_digits=9, decimal_places=0, blank=True, null=True)
    empresa_direccion       = models.CharField("Dirección de la Empresa", max_length=255, blank=True, null=True)
    empresa_inscripcion     = models.CharField("Inscripción:", max_length=500, blank=True, null=True)
    empresa_correo_p        = models.EmailField("Dirección de Correo Primaria:", blank=True, null=True)
    empresa_correo_s        = models.EmailField("Dirección de Correo Alternativa:", blank=True, null=True)


    def __str__(self):
        return self.empresa_nombre
    
    def get_absolute_url(self):
        return f"/polizas/crear/empresa/{self.id}"

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
    
    poliza_fecha = models.DateField("Fecha")
    poliza_expediente = models.CharField("Expediente", max_length=18)
    poliza_numero = models.IntegerField("Número de Póliza")
    poliza_concepto = models.CharField("Concepto", max_length=1, choices=CONCEPTO)
    poliza_anexo = models.CharField("Anexo de Póliza", max_length=40, blank=True, null=True)
    poliza_recibo = models.CharField("Número de Recibo", max_length=100)
    poliza_aseguradora = models.ForeignKey("Aseguradora", on_delete=models.CASCADE)
    poliza_tomador = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    poliza_obra = models.ForeignKey("Obra", on_delete=models.CASCADE)
    poliza_monto_pesos = models.DecimalField("Monto Sustituido en Pesos", max_digits=15, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    poliza_monto_uvi = models.DecimalField("Monto Sustituido en UVI", max_digits=15, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    poliza_digital = models.FileField(upload_to=generate_name_poliza, max_length=500, null=True, blank=True)
    poliza_creador = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    poliza_editor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="poliza_editor", editable=False)
    
    def __str__(self):
        return f"{self.poliza_numero} - {self.poliza_aseguradora.aseguradora_nombre} - {self.poliza_obra.obra_nombre} - {self.poliza_tomador.empresa_nombre} "

    def get_absolute_url(self):
        return f"/polizas/crear/poliza/estado/{self.id}"

class Poliza_Movimiento(models.Model):
    class Meta:
        verbose_name = "Poliza_Movimiento"
        verbose_name_plural = "Polizas_Movimiento"
    
    poliza_movimiento_fecha     = models.DateField("Fecha")
    poliza_movimiento_receptor  = models.ForeignKey("Receptor", on_delete=models.CASCADE)
    poliza_movimiento_area      = models.ForeignKey("Area", on_delete=models.CASCADE)
    poliza_movimiento_editor    = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    poliza_movimiento_numero    = models.ForeignKey("Poliza", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.poliza_movimiento_numero} - {self.poliza_movimiento_area} - ({self.poliza_movimiento_fecha})"
    
    def get_absolute_url(self):
        return f"/polizas/crear/poliza/estado/{self.poliza_movimiento_numero.id}"

class LegacyPoliza(models.Model):
    CONCEPTO = (
        ("C", "Garantía de Ejecución de Contrato"),
        ("F", "Garantía de Sustitución de Fondo de Reparo"),
        ("A", "Garantía de Anticipo Financiero")
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=["legacy_poliza_expediente", "legacy_poliza_fecha", "legacy_poliza_numero", "legacy_poliza_aseguradora","legacy_poliza_receptor"], name="legacy-poliza-constraint")]
        verbose_name = "Legacy_Póliza"
        verbose_name_plural = "Legacy_Pólizas"

    legacy_poliza_fecha            = models.DateField("Fecha")
    legacy_poliza_expediente       = models.CharField("Número de Expediente", max_length=17)
    legacy_poliza_receptor         = models.ForeignKey("Receptor", on_delete=models.CASCADE)
    legacy_poliza_area             = models.ForeignKey("Area", on_delete=models.CASCADE)
    legacy_poliza_numero           = models.IntegerField("Número de Póliza")
    legacy_poliza_concepto         = models.CharField("Concepto", max_length=1, choices=CONCEPTO)
    legacy_poliza_anexo            = models.CharField("Anexo de póliza", max_length=40, blank=True, null=True)
    legacy_poliza_recibo           = models.CharField("Número de Recibo", max_length=100)
    legacy_poliza_aseguradora      = models.ForeignKey("Aseguradora", on_delete=models.CASCADE)
    legacy_poliza_tomador          = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    legacy_poliza_obra_nombre      = models.TextField("Obra")
    legacy_poliza_obra_convenio    = models.CharField("Convenio", max_length=50, blank=True, null=True)
    legacy_poliza_obra_expediente  = models.CharField("Número de Expediente de la Obra", max_length=17, blank=True, null=True)
    legacy_poliza_monto_pesos      = models.DecimalField("Monto Sustituido Pesos", max_digits=12, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    legacy_poliza_monto_uvi        = models.DecimalField("Monto Sustituido UVI", max_digits=12, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    legacy_poliza_creador          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    legacy_poliza_editor           = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="legacy_poliza_editor", editable=False)
    
class Programa(models.Model):
    class Meta:
        verbose_name = "Programa"
        verbose_name_plural = "Programas"
    
    programa_nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.programa_nombre
    
    def get_absolute_url(self):
        return f"/polizas/crear/programa/{self.id}"
    
class Region(models.Model):
    class Meta:
        ordering = ["region_numero"]
        verbose_name_plural = "Region"
    
    region_numero   = models.CharField("Número Región", max_length=10)

    def __str__(self):
        return self.region_numero
    
    def get_absolute_url(self):
        return f"/polizas/crear/region/{self.id}"


class Departamento(models.Model):
    class Meta:
        ordering			= ["departamento_nombre"]
        verbose_name_plural = "Departamentos"

    id					= models.IntegerField(unique=True, primary_key=True)
    departamento_nombre = models.TextField("Nombre Departamento")

    def __str__(self):
        return self.departamento_nombre

    def get_abolute_url(self):
        return f"/polizas/crear/departamento/{self.id}"

class Localidad(models.Model):
    class Meta:
        ordering			= ["localidad_nombre"]
        verbose_name_plural = "Localidades"

    localidad_nombre		= models.TextField("Nombre Localidad")
    id                      = models.IntegerField(unique=True, primary_key=True) 
    localidad_centroide_lat	= models.DecimalField(max_digits=15, decimal_places=13,blank=True, null=True)
    localidad_centroide_lon	= models.DecimalField(max_digits=15, decimal_places=13,blank=True, null=True)
    localidad_funcion       = models.CharField(max_length=40,blank=True, null=True)
    localidad_departamento	= models.ForeignKey("Departamento", on_delete=models.RESTRICT)
    localidad_municipio     = models.ForeignKey("Municipio", on_delete=models.CASCADE)

    def __str__(self):
        return self.localidad_nombre
    # return "{} - Departamento {}".format(self.localidad_nombre, self.localidad_departamento)

    def get_absolute_url(self):
        return f"/polizas/crear/localidad/{self.id}"

class Municipio(models.Model):
    class Meta:
        ordering 			= ["municipio_nombre"]
        verbose_name_plural = "Municipios"

    municipio_nombre        = models.CharField(max_length=40)
    id                      = models.IntegerField(unique=True, primary_key=True)
    municipio_departamento  = models.ForeignKey("Departamento", on_delete=models.CASCADE)
    municipio_region        = models.ForeignKey("Region", on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.municipio_nombre
    
    def get_absolute_url(self):
        return f"/polizas/crear/municipio/{self.id}"

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

    obra_nombre			                = models.TextField("Nombre de la Obra tal como figura en el contrato")
    obra_soluciones		                = models.DecimalField("Cantidad de soluciones", max_digits=4, decimal_places=0, null=True, blank=True)
    obra_empresa		                = models.ForeignKey("Empresa", on_delete=models.CASCADE, verbose_name="Empresa")
    obra_region                         = models.ForeignKey("Region", on_delete=models.CASCADE, verbose_name="Región", null=True, blank=True)
    obra_departamento_m                 = models.ManyToManyField("Departamento", related_name="obra_departamento", verbose_name="Departamento", blank=True)
    obra_municipio_m                    = models.ManyToManyField("Municipio", related_name="obra_municipio", verbose_name="Municipio", blank=True)
    obra_localidad_m	                = models.ManyToManyField("Localidad", related_name="obra_localidad", verbose_name="Localidad", blank=True)
    obra_conjunto                       = models.ForeignKey("ConjuntoLicitado", on_delete=models.DO_NOTHING, null=True, blank=True)
    obra_grupo                          = models.CharField("Grupo", max_length=4, blank=True, null=True)
    obra_plazo                          = models.CharField("Plazo de Ejecución", max_length=10, blank=True, null=True)
    obra_programa		                = models.ForeignKey("Programa", on_delete=models.CASCADE)
    obra_convenio		                = models.CharField("Convenio/ACU", max_length=60, blank=True, null=True)
    obra_expediente 	                = models.CharField("Expediente", max_length=18)
    obra_resolucion                     = models.CharField("Resolución de Adjudicación", max_length=15, blank=True, null=True)
    obra_licitacion_tipo                = models.CharField("Compulsa", max_length=1, choices=COMPULSA, blank=True, null=True)
    obra_licitacion_numero              = models.DecimalField("Número de Licitación", max_digits=3, decimal_places=0, blank=True, null=True)
    obra_licitacion_ano                 = models.DecimalField("Año de Licitación", max_digits=4, decimal_places=0, blank=True, null=True)
    obra_nomenclatura                   = models.CharField("Nomenclatura Catastral", max_length=1000, blank=True, null=True)  
    obra_nomenclatura_plano             = models.CharField("Número de Plano", max_length=10, blank=True, null=True)
    obra_fecha_entrega                  = models.DateField("Fecha de Entrega de la Obra", blank=True, null=True)
    obra_fecha_contrato                 = models.DateField("Fecha de Firma de Contrato", blank=True, null=True)
    obra_expediente_costo               = models.CharField("Expediente de Costos", max_length=18, blank=True, null=True)
    obra_inspector                      = models.ManyToManyField("Agente", related_name="obra_inspector", verbose_name="Inspector")
    obra_observaciones                  = models.TextField("Observaciones:", blank=True, null=True)
    obra_contrato_nacion_pesos          = models.DecimalField("Monto Nación en Pesos: ", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_nacion_uvi            = models.DecimalField("Monto Nación en UVI: ", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_nacion_uvi_fecha      = models.DateField("Fecha UVI Nación: ", blank=True, null=True)
    obra_contrato_provincia_pesos       = models.DecimalField("Monto Provincia en Pesos: ", max_digits=12 ,decimal_places=2, default=0 , validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_provincia_uvi         = models.DecimalField("Monto Provincia en UVI: ", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_provincia_uvi_fecha   = models.DateField("Fecha UVI Provicia: ", blank=True, null=True)
    obra_contrato_terceros_pesos        = models.DecimalField("Monto Terceros en Pesos: ", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_terceros_uvi          = models.DecimalField("Monto Terceros en UVI: ", max_digits=12 ,decimal_places=2, default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    obra_contrato_terceros_uvi_fecha    = models.DateField("Fecha UVI Terceros: ", blank=True, null=True)
    obra_contrato_total_pesos           = models.DecimalField("Monto Total Pesos", max_digits=12, decimal_places=2, default=0, editable=False)
    obra_contrato_total_uvi             = models.DecimalField("Monto Total UVI", max_digits=12, decimal_places=2, default=0, editable=False)
    obra_principal                      = models.ManyToManyField("Obra", related_name="obra_madre", verbose_name="Obra Madre", blank=True)

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
    
    def __str__(self):
        localidades = ", ".join(str(localidad) for localidad in self.obra_localidad_m.all())
        return f"({self.obra_convenio if self.obra_convenio else ''}) {self.obra_nombre} - {self.obra_empresa}"
    
    def save(self):
        self.obra_contrato_total_pesos = self.obra_contrato_nacion_pesos + self.obra_contrato_terceros_pesos + self.obra_contrato_provincia_pesos
        self.obra_contrato_total_uvi = self.obra_contrato_nacion_uvi + self.obra_contrato_terceros_uvi + self.obra_contrato_provincia_uvi
        return super(Obra, self).save()

    def lista_localidades(self):
        return ", ".join(str(localidad) for localidad in self.obra_localidad_m.all())
    
    def get_absolute_url(self):
        return f"/polizas/crear/obra/estado/{self.id}"

class Prototipo(models.Model):
    TIPO = (
        ("1", "1 Dormitorio"),
        ("2", "2 Dormitorios"),
        ("3", "3 Dormitorios"),
        ("4", "4 Dormitorios"),
        ("o", "Otro")
    )

    class meta:
        verbose_name = "Prototipo Habitacional"
        verbose_name_plural = "Prototipos Habitacionales"
    
    prototipo_obra          = models.ForeignKey("Obra", on_delete=models.DO_NOTHING)
    prototipo_tipo          = models.CharField("Tipo de Prototipo:", max_length=1, choices=TIPO)
    prototipo_cantidad      = models.DecimalField("Cantidad del Prototipo:", max_digits=3, decimal_places=0)
    prototipo_superficie    = models.DecimalField("Superficie del Prototipo: ", max_digits=3, decimal_places=0)
    prototipo_uvi           = models.DecimalField("UVIs x M2:", max_digits=5, decimal_places=2)
    prototipo_incremento    = models.DecimalField("Incremento Porcentual por Infraestructura:", max_digits=2, decimal_places=0)
    prototipo_discapacitado = models.BooleanField("Es Prototipo para Discapacitado: ", default=False)


class Agente(models.Model):
    class Meta:
        verbose_name_plural = "Agentes"

    PROFESION = (
        ("A", "Arquitecto"),
        ("IC", "Ingeniero Civil"),
        ("IE", "Ingeniero Electromecánico"),
        ("MO", "Maestro Mayor de Obras")
    )

    agente_nombre 			= models.CharField("Nombre/s:", max_length=60)
    agente_apellido			= models.CharField("Apellido/s:", max_length=60)
    agente_dni				= models.DecimalField("DNI:", max_digits=9, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(0)])
    agente_telefono 		= models.CharField("Telefono:", max_length=20, blank=True, null=True)
    agente_email 			= models.EmailField("Email:", blank=True,null=True)
    agente_profesion		= models.CharField("Profesion", max_length=2, choices=PROFESION, default=None, blank=True, null=True)
    agente_matricula		= models.CharField("Matricula Profesional", max_length=10, blank=True, null=True)
    agente_nombre_completo  = models.CharField("Nombre Completo", max_length=200, editable=False, blank=True, null=True)

    def save(self):
        self.agente_nombre_completo = f"{self.agente_nombre} {self.agente_apellido}"
        return super(Agente, self).save()
    
    def __str__(self):
        return f"{self.agente_nombre} {self.agente_apellido}"

    def get_absolute_url(self):
        return f"/polizas/crear/agente/{self.id}"
	
class CertificadoRubro(models.Model):
    class Meta:
        verbose_name_plural = "Rubros"
    
    certificadorubro_nombre = models.CharField("Rubro", max_length=100)
    certificadorubro_nombre_corto = models.CharField("Rubro Corto", max_length=1)

    def __str__(self):
        return f"{self.certificadorubro_nombre}"

class CertificadoFinanciamiento(models.Model):
    class Meta:
        verbose_name_plural = "Financiamiento"
    
    certificadofinanciamiento_nombre = models.CharField("Financiamiento", max_length=100)
    certificadofinanciamiento_nombre_corto = models.CharField("Financiamiento Corto", max_length=1)

    def __str__(self):
        return f"{self.certificadofinanciamiento_nombre}"
    
class Certificado(models.Model):
    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        get_latest_by = "certificado_fecha"
    
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

    certificado_obra                = models.ForeignKey("Obra", on_delete=models.CASCADE)
    certificado_financiamiento      = models.CharField("Financiamiento", max_length=1, choices=FINANCIAMIENTO, default="N")
    certificado_rubro               = models.CharField("Rubro", max_length=1, choices=RUBRO, default="V") # Obsoleto -> se migro a una tabla aparte(carga.models.CertificadoRubro)
    certificado_rubro_db            = models.ForeignKey("CertificadoRubro", on_delete=models.DO_NOTHING, default=1, verbose_name="Rubro")
    certificado_rubro_anticipo      = models.DecimalField("Anticipo N°", max_digits=3, decimal_places=0, null=True, blank=True, validators=[MinValueValidator(0)])
    certificado_rubro_obra          = models.DecimalField("Obra N°", max_digits=3, decimal_places=0, null=True, blank=True, validators=[MinValueValidator(0)])
    certificado_rubro_devanticipo   = models.DecimalField("Devolución de Anticipo N°", max_digits=3, decimal_places=0, null=True, blank=True, validators=[MinValueValidator(0)])
    certificado_expediente          = models.CharField("Número de Expediente", max_length=18)
    certificado_periodo             = models.CharField("Periodo", max_length=13, null=True, blank=True)
    certificado_monto_pesos         = models.DecimalField("Monto en Pesos", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    certificado_mes_pct             = models.DecimalField("Mes %", max_digits=5, decimal_places=2, default=0, validators=[MaxValueValidator(100)])
    certificado_ante_pct            = models.DecimalField("Anterior %", max_digits=5, decimal_places=2, default=0, validators=[MaxValueValidator(100)])
    certificado_acum_pct            = models.DecimalField("Acumulado %", max_digits=5, decimal_places=2, default=0, validators=[MaxValueValidator(100)])
    certificado_devolucion_expte    = models.CharField("Número de Expediente Devolución", max_length=18, null=True, blank=True)
    certificado_devolucion_monto    = models.DecimalField("Monto Devolución en Pesos", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    certificado_devolucion_monto_uvi = models.DecimalField("Monto Devolución en UVI", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    certificado_monto_uvi           = models.DecimalField("Monto en UVI", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    certificado_fecha               = models.DateField("Fecha", default=timezone.now)
    certificado_monto_cobrar        = models.DecimalField("Monto a Cobrar Pesos", max_digits=12, decimal_places=2, default=0, editable=False)
    certificado_monto_cobrar_uvi    = models.DecimalField("Monto a Cobrar UVI", max_digits=12, decimal_places=2, default=0, editable=False)
    certificado_digital             = models.FileField(upload_to=generate_name, max_length=500, null=True, blank=True)
    certificado_creador             = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    certificado_editor              = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="certificado_editor", editable=False)
    certificado_fecha_carga         = models.DateField("Fecha de carga", default=timezone.now)
    certificado_fecha_carga_legacy  = models.BooleanField("Es Certificado Viejo", default=False)
    

    def save(self):
        # certificado_monto_cobrar = certificado_monto_pesos + certificado_devolucion_monto
        # certificado_set.aggregate(Sum(F("certificado_monto_pesos"), output_field=FloatField()))

        self.certificado_monto_cobrar = self.certificado_monto_pesos - self.certificado_devolucion_monto
        self.certificado_monto_cobrar_uvi = self.certificado_monto_uvi - self.certificado_devolucion_monto_uvi 
        return super(Certificado, self).save()
    
    def __str__(self):
        return f"{self.certificado_obra} - {self.certificado_expediente} - Rubro: {self.get_certificado_rubro_display()} - Financiamiento: {self.get_certificado_financiamiento_display()} - Ant. N°{self.certificado_rubro_anticipo} - Ob. N°{self.certificado_rubro_obra} - Dev. N°{self.certificado_rubro_devanticipo}"
    
    def get_absolute_url(self):
        return f"/polizas/crear/certificado/{self.id}"

class ConjuntoLicitado(models.Model):
    conjunto_nombre = models.TextField("Nombre")
    conjunto_soluciones = models.DecimalField("Cantidad de Soluciones", max_digits=5, decimal_places=0, default=0, null=True, blank=True)
    conjunto_resolucion = models.CharField("Resolucion", max_length=15, null=True, blank=True)
    conjunto_subconjunto = models.ForeignKey("ConjuntoLicitado", on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f"{self.conjunto_nombre}"
    
    def get_absolute_url(self):
        return f"/polizas/crear/conjunto/{self.id}"

class PlanDeTrabajos(models.Model):
    """
    Ver como verga construir el plan de trabajos
    """
    class Meta:
        verbose_name_plural = "Plan de Trabajos"

    trabajos_obra = models.ForeignKey("Obra", on_delete=models.DO_NOTHING)

class Contrato(models.Model):
    class Meta:
        verbose_name_plural = "Contratos"

    contrato_obra = models.ForeignKey("Obra", on_delete=models.CASCADE)
    contrato_fecha = models.DateField("Fecha",default=timezone.now)
    contrato_descripcion = models.CharField("Descripción", max_length=600, default="")
    contrato_resolucion = models.CharField("Resolución Aprobatoria", max_length=15, blank=True, null=True)
    contrato_autocarga = models.BooleanField("Contrato importado de formato anterior", editable=False, default=False)
    contrato_decreto = models.CharField("Decreto Aprobatorio(Si Tuviera)", max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.contrato_descripcion} - {self.contrato_obra}"

class ContratoMonto(models.Model):
    class Meta:
        verbose_name_plural = "Montos de Contrato"
    
    contratomonto_contrato = models.ForeignKey("Contrato", on_delete=models.CASCADE)
    contratomonto_rubro = models.ForeignKey("CertificadoRubro", on_delete=models.CASCADE)
    contratomonto_financiamiento = models.ForeignKey("CertificadoFinanciamiento", on_delete=models.CASCADE)
    contratomonto_pesos = models.DecimalField("Monto Pesos", max_digits=15, decimal_places=2, default=0)
    contratomonto_uvi = models.DecimalField("Monto UVI", max_digits=15, decimal_places=2, default=0)
    contratomonto_uvi_fecha = models.DateField("Fecha UVI:", blank=True, null=True)

    def __str__(self):
        return f"{self.contratomonto_rubro}({self.contratomonto_financiamiento}) - {self.contratomonto_contrato}"

class ContratoRubro(models.Model):
    class Meta:
        verbose_name_plural = "Rubros de Contrato"
    
    contratorubro_tipo = models.CharField("Rubro:", max_length=100)

    def __str__(self):
        return f"{self.contratorubro_tipo}"
    
class ContratosDigitales(models.Model):
    class Meta:
        verbose_name_plural = "Contratos Digitales"
    
    contratodigital_obra = models.ManyToManyField("Obra", related_name="obra_contratos", verbose_name="Obras", blank=True)
    contratodigital_nombre_archivo = models.CharField("Nombre del Archivo", max_length=100, blank=True, null=True)
    contratodigital_descripcion = models.TextField("Descripción")
    contratodigital_tipo = models.ForeignKey("ContratoRubro", on_delete=models.CASCADE)
    contratodigital_archivo = models.FileField(upload_to=generate_name_contratos, max_length=500)
    contratodigital_creador = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    contratodigital_editor  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="contratodigital_editor", editable=False)


class ResolucionesDigitales(models.Model):
    class Meta:
        verbose_name_plural = "Resoluciones Digitales"
    
    resoluciondigital_obra          = models.ManyToManyField("Obra", related_name="obra_resoluciones", verbose_name="Obras", blank=True)
    resoluciondigital_descripcion   = models.TextField("Descripción")
    resoluciondigital_numero        = models.CharField("Resolución", max_length=15)
    resoluciondigital_archivo       = models.FileField(upload_to=generate_name_resoluciones, max_length=500)
    resoluciondigital_creador       = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    resoluciondigital_editor        = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="resoluciondigital_editor", editable=False)
    
    def __str__(self):
        return f"{self.resoluciondigital_numero}"
class Uvi(models.Model):
    class Meta:
        verbose_name_plural = "UVI"

    uvi_fecha = models.DateField("Fecha UVI:")
    uvi_valor = models.DecimalField("Valor", max_digits=15, decimal_places=2)

class INDEC(models.Model):

    class Meta:
        verbose_name_plural = "INDEC"

    mes                         = models.DateField("Fecha de Medición")
    indec_manodeobra            = models.DecimalField("Mano de Obra", max_digits=20, decimal_places=10)
    indec_albanileria           = models.DecimalField("Albañilería", max_digits=20, decimal_places=10)
    indec_carpinterías          = models.DecimalField("Carpinterías", max_digits=20, decimal_places=10)
    indec_andamios              = models.DecimalField("Andamios", max_digits=20, decimal_places=10)
    indec_iluminación           = models.DecimalField("Artefactos de iluminación y cableado", max_digits=20, decimal_places=10)
    indec_pvc                   = models.DecimalField("Caños de PVC para instalaciones varias", max_digits=20, decimal_places=10)
    indec_gastos                = models.DecimalField("Gastos Generales", max_digits=20, decimal_places=10)
    indec_artefactos            = models.DecimalField("Artefactos para baño y grifería", max_digits=20, decimal_places=10)
    indec_hormigon              = models.DecimalField("Hormigón", max_digits=20, decimal_places=10)
    indec_valvulas              = models.DecimalField("Válvulas de bronce", max_digits=20, decimal_places=10)
    indec_electrobombas         = models.DecimalField("Electrobombas", max_digits=20, decimal_places=10)
    indec_quimicos              = models.DecimalField("Productos Químicos", max_digits=20, decimal_places=10)
    indec_motores               = models.DecimalField("Motores eléctricos y equipos de aire acondicionado", max_digits=20, decimal_places=10)
    indec_asfaltos              = models.DecimalField("Asfaltos, combustibles y lubricantes", max_digits=20, decimal_places=10)
    indec_medidores             = models.DecimalField("Medidores de caudal", max_digits=20, decimal_places=10)
    indec_membrana              = models.DecimalField("Membrana impermeabilizante", max_digits=20, decimal_places=10)
    indec_equipo                = models.DecimalField("Equipo - Amortización de equipo", max_digits=20,decimal_places=10)
    indec_pisos                 = models.DecimalField("Pisos y revestimientos", max_digits=20, decimal_places=10)
    indec_aceros                = models.DecimalField("Aceros - Hierro aletado", max_digits=20, decimal_places=10)
    indec_cemento               = models.DecimalField("Cemento", max_digits=20, decimal_places=10)
    indec_arena                 = models.DecimalField("Arena", max_digits=20, decimal_places=10)
    indec_costo_financiero      = models.DecimalField("Costo Financiero", max_digits=20, decimal_places=10, default=18.85)
    indec_transporte            = models.DecimalField("Transporte", max_digits=20, decimal_places=10, default=134.98)

    def __str__(self):
        return f"{self.mes}"