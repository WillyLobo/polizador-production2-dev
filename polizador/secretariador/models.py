from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from secretariador.functions import FileValidator, CuitValidator
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
import os
from django.db.models.fields.generated import GeneratedField

# Funciones
def generate_name_decretos(instance, filename):
    """
    Generates a name for a decree file based on the given instance and filename.

    Parameters:
        instance (object): The instance of the decree.
        filename (str): The original filename of the decree.

    Returns:
        str: The generated name for the decree file.
    """
    directorio = "instrumentoslegales/decretos/"
    filename = f"{instance.instrumentolegaldecretos_numero}-{instance.instrumentolegaldecretos_ano}-{instance.instrumentolegaldecretos_tipo}.pdf"
    name = os.path.join(directorio, filename)
    return name
def generate_name_resoluciones(instance, filename):
    """
    Generates a name for a resolution file based on the given instance and filename.

    Parameters:
        instance (object): The instance of the resolution.
        filename (str): The original filename of the resolution.

    Returns:
        str: The generated name for the resolution file.
    """
    directorio = "instrumentoslegales/resoluciones/"
    filename = f"{instance.instrumentolegalresoluciones_numero}-{instance.instrumentolegalresoluciones_ano}-{instance.instrumentolegalresoluciones_tipo}.pdf"
    name = os.path.join(directorio, filename)
    return name
def date_validation(value):
    """
    Validates if the provided date value is not earlier than the current date.
    :param value: The date value to be validated.
    :raises ValidationError: If the value is earlier than the current date.
    """
    if value < datetime.now().date():
        raise ValidationError('%(value)s no puede ser menor a la fecha actual', params={'value': value})

class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"

# Modelos
class InstrumentosLegalesResoluciones(models.Model):
    class Meta:
        verbose_name = "Instrumento Legal(Resolución)"
        verbose_name_plural = "Instrumentos Legales(Resoluciones)"
        constraints = [
            models.UniqueConstraint(
                fields=["instrumentolegalresoluciones_tipo", "instrumentolegalresoluciones_numero", "instrumentolegalresoluciones_ano"],
                name='unique_resolucion_1'
            ),
        ]

    TIPO = (
        ("P", "Resolución de Presidencia"),
        ("D", "Resolución de Directorio")
    )

    instrumentolegalresoluciones_tipo = models.CharField("Tipo", max_length=1, choices=TIPO, default="P")
    instrumentolegalresoluciones_numero = models.CharField("Número", max_length=7)
    instrumentolegalresoluciones_ano = models.CharField("Año", max_length=5)
    instrumentolegalresoluciones_fecha_aprobacion = models.DateField("Fecha de Aprobación", default=timezone.now)
    instrumentolegalresoluciones_descripcion = models.CharField("Descripción", max_length=600, default="")
    instrumentolegalresoluciones = models.FileField(upload_to=generate_name_resoluciones, max_length=500, validators=[FileValidator(max_size=1024*1024*14, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
    instrumentolegalresoluciones_str = GeneratedField(
        expression=ConcatOp('instrumentolegalresoluciones_numero', models.Value(" - "), 'instrumentolegalresoluciones_ano', models.Value(" - "), 'instrumentolegalresoluciones_tipo'),
        output_field=models.TextField(),
        db_persist=True,
    )

    def __str__(self):
        return f"{self.get_instrumentolegalresoluciones_tipo_display()} Nº{self.instrumentolegalresoluciones_numero}/{self.instrumentolegalresoluciones_ano}"

class InstrumentosLegalesDecretos(models.Model):
    class Meta:
        verbose_name = "Instrumento Legal(Decreto)"
        verbose_name_plural = "Instrumentos Legales(Decretos)"
        constraints = [
            models.UniqueConstraint(
                fields=["instrumentolegaldecretos_tipo", "instrumentolegaldecretos_numero", "instrumentolegaldecretos_ano"],
                name='unique_decretos_1'
            ),
        ]
        get_latest_by = ["instrumentolegaldecretos_ano", "instrumentolegaldecretos_numero"]

    TIPO = (
        ("N", "Decreto Nacional"),
        ("P", "Decreto Provincial")
    )

    instrumentolegaldecretos_tipo = models.CharField("Tipo", max_length=1, choices=TIPO, default="P")
    instrumentolegaldecretos_numero = models.CharField("Número", max_length=7)
    instrumentolegaldecretos_ano = models.CharField("Año", max_length=5)
    instrumentolegaldecretos_fecha_aprobacion = models.DateField("Fecha de Aprobación", default=timezone.now)
    instrumentolegaldecretos_descripcion = models.CharField("Descripción", max_length=600, default="Escala de viáticos")
    instrumentolegaldecretos = models.FileField(upload_to=generate_name_decretos, max_length=500, validators=[FileValidator(max_size=1024*1024*14, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
    instrumentolegaldecretos_str = GeneratedField(
        expression=ConcatOp('instrumentolegaldecretos_numero', models.Value(" - "), 'instrumentolegaldecretos_ano', models.Value(" - "), 'instrumentolegaldecretos_tipo'),
        output_field=models.TextField(),
        db_persist=True,
    )

    def __str__(self):
        return f"{self.get_instrumentolegaldecretos_tipo_display()} Nº{self.instrumentolegaldecretos_numero}/{self.instrumentolegaldecretos_ano}"
    
class MontoViaticoDiario(models.Model):
    class Meta:
        verbose_name = "Monto diario de Viático"
        verbose_name_plural = "Monto diario de Viáticos"
    
    montoviaticodiario_estrato_uno_interior     = models.DecimalField("Viatico diario Estrato I dentro de la Provincia", max_digits=12, decimal_places=2, default=0)
    montoviaticodiario_estrato_dos_interior     = models.DecimalField("Viatico diario Estrato II dentro de la Provincia", max_digits=12, decimal_places=2, default=0)
    montoviaticodiario_estrato_tres_interior    = models.DecimalField("Viatico diario Estrato III dentro de la Provincia", max_digits=12, decimal_places=2, default=0)
    montoviaticodiario_estrato_cuatro_interior  = models.DecimalField("Viatico diario Estrato IV dentro de la Provincia", max_digits=12, decimal_places=2, default=0)
    montoviaticodiario_estrato_uno_exterior     = models.DecimalField("Viatico diario Estrato I fuera de la Provincia", max_digits=12, decimal_places=2, default=0)
    montoviaticodiario_estrato_dos_exterior     = models.DecimalField("Viatico diario Estrato II fuera de la Provincia", max_digits=12, decimal_places=2, default=0)
    montoviaticodiario_estrato_tres_exterior    = models.DecimalField("Viatico diario Estrato III fuera de la Provincia", max_digits=12, decimal_places=2, default=0)
    montoviaticodiario_estrato_cuatro_exterior  = models.DecimalField("Viatico diario Estrato IV fuera de la Provincia", max_digits=12, decimal_places=2, default=0)
    montoviaticodiario_decreto_reglamentario    = models.ForeignKey("InstrumentosLegalesDecretos", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.montoviaticodiario_decreto_reglamentario}"

class Comisionado(models.Model):
    class Meta:
        ordering = ("comisionado_apellidos",)
        verbose_name = "Comisionado"
        verbose_name_plural = "Comisionados"
    SEXO = (
        ("M", "Masculino"),
        ("F", "Femenino")
    )

    comisionado_nombres = models.CharField("Nombres", max_length=120)
    comisionado_apellidos = models.CharField("Apellidos", max_length=120)
    comisionado_abreviatura = models.CharField("Abreviatura", max_length=10, help_text="(Sr., Sra., Dr., Dra., Etc.)")
    comisionado_sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    comisionado_cargo = models.ForeignKey("Organigrama", on_delete=models.CASCADE)
    comisionado_dni = models.DecimalField("DNI:", max_digits=9, decimal_places=0, validators=[MinValueValidator(0)])
    comisionado_cuit = models.CharField("CUIT", max_length=13, validators=[CuitValidator()])
    comisionado_nombreyapellido = GeneratedField(
        expression=ConcatOp('comisionado_apellidos', models.Value(", "), 'comisionado_nombres'),
        output_field=models.TextField(),
        db_persist=True,
    )

    def __str__(self):
        return f"{self.comisionado_apellidos}, {self.comisionado_nombres}"
    
    def nombreydni(self):
        return f"{self.comisionado_abreviatura} {self.comisionado_apellidos}, {self.comisionado_nombres}-DNI Nº{self.comisionado_dni}"

    def comisionado_nombre(self):
        return f"{self.comisionado_apellidos}, {self.comisionado_nombres}"

class Organigrama(models.Model):
    organigrama_cargo = models.CharField("Cargo", max_length=120)
    organigrama_escalafon = models.DecimalField("Escalafón", max_digits=1, decimal_places=0, default=2)

    def __str__(self):
        return self.organigrama_cargo

class Vehiculo(models.Model):
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
    
    VEHICULO = (
        ("E", "Empresa"),
        ("O", "Oficial"),
        ("P", "Particular"),
    )

    vehiculo_caracter = models.CharField("Vehiculo Designación", max_length=1, choices=VEHICULO, default="O")
    vehiculo_modelo = models.CharField("Modelo", max_length=100)
    vehiculo_patente = models.CharField("Patente", max_length=9)
    vehiculo_poliza = models.CharField("Número de Póliza", max_length=100, null=True, blank=True)
    vehiculo_poliza_aseguradora = models.ForeignKey("carga.Aseguradora", on_delete=models.CASCADE, null=True, blank=True)
    vehiculo_str = GeneratedField(
        expression=ConcatOp('vehiculo_modelo', models.Value(" - "), 'vehiculo_patente'),
        output_field=models.TextField(),
        db_persist=True,
    )

    def __str__(self):
        return f"{self.vehiculo_modelo} - {self.vehiculo_patente}"

class Solicitud(models.Model):
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        constraints = [
            models.UniqueConstraint(
                fields=["solicitud_actuacion"],
                name='unique_solicitud_1'
            ),
        ]
    solicitud_actuacion = models.CharField("Actuación", max_length=18)
    solicitud_solicitante = models.ForeignKey("Comisionado", on_delete=models.CASCADE) # Encargado del area solicitante
    solicitud_provincia = models.ForeignKey("carga.Provincia", on_delete=models.CASCADE)
    solicitud_localidades = models.ManyToManyField("carga.Localidad")
    solicitud_decreto_viaticos = models.ForeignKey("MontoViaticoDiario", on_delete=models.CASCADE)
    solicitud_fecha_desde = models.DateField("Fecha Inicio")
    solicitud_fecha_hasta = models.DateField("Fecha Regreso")
    solicitud_tareas = models.TextField("Tareas a Realizar", help_text="... a fin de #Texto ingresado en el formulario#")
    solicitud_vehiculo = models.ForeignKey("Vehiculo", on_delete=models.CASCADE)
    solicitud_dia_inhabil = models.BooleanField("Dia Inhábil", help_text="Tildar si es un diá de no laboral")
    solicitud_resolucion = models.ForeignKey("InstrumentosLegalesResoluciones", verbose_name="Resolución Aprobada", on_delete=models.CASCADE, blank=True, null=True)
    solicitud_viaticos_total = GeneratedField(
        expression=models.F('solicitud_fecha_hasta') - models.F('solicitud_fecha_desde') + timedelta(days=1),
        output_field=models.DurationField(),
        db_persist=True,
    )
    
    def solicitud_fechas(self):
        fechas = [self.solicitud_fecha_desde+timedelta(days=x) for x in range((self.solicitud_fecha_hasta-self.solicitud_fecha_desde).days+1)]
        fechas = [datetime.strftime(fecha, "%d/%m/%Y") for fecha in fechas]
        return fechas
    def cantidad_de_dias(self):
        dias = (self.solicitud_fecha_hasta-self.solicitud_fecha_desde).days+1
        return dias
    
    def monto_viaticos(self): # ADD RANK CHECK!!!
        monto_diario = self.solicitud_decreto_viaticos.montoviaticodiario_estrato_dos_interior
        return self.cantidad_de_dias * monto_diario
    
    def get_comisionados(self):
        serialized_q = self.comisionadosolicitud_set.values_list("comisionadosolicitud_nombre__comisionado_nombreyapellido", flat=True)
        return list(serialized_q)

    def clean(self):
        self.solicitud_actuacion = self.solicitud_actuacion.upper()

    def __str__(self):
        return f"{self.solicitud_actuacion}"

class ComisionadoSolicitud(models.Model):
    class Meta:
        verbose_name = "Comisionado Solicitud"
        verbose_name_plural = "Comisionado Solicitudes"

    comisionadosolicitud_foreign = models.ForeignKey("Solicitud", on_delete=models.CASCADE, null=True, blank=True)
    comisionadosolicitud_incorporacion_foreign = models.ForeignKey("Incorporacion", on_delete=models.CASCADE, null=True, blank=True)
    comisionadosolicitud_nombre = models.ForeignKey("Comisionado", on_delete=models.CASCADE)
    comisionadosolicitud_colaborador = models.BooleanField("Es colaborador?")
    comisionadosolicitud_chofer = models.BooleanField("Es Chofer?")
    comisionadosolicitud_combustible = models.DecimalField("Combustible", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    comisionadosolicitud_gastos = models.DecimalField("Gastos", max_digits=12, decimal_places=2, default=0, null=True, blank=True)

    def valor_viatico_dia(self):
        gabinete = self.comisionadosolicitud_nombre.comisionado_cargo.organigrama_cargo
        estrato = self.comisionadosolicitud_nombre.comisionado_cargo.organigrama_escalafon
        if gabinete == "Vocal" or gabinete == "Presidente":
            estrato_decreto = 0
        else:
            if estrato == 1:
                estrato_decreto = self.comisionadosolicitud_foreign.solicitud_decreto_viaticos.montoviaticodiario_estrato_uno_interior
            elif estrato == 2:
                estrato_decreto = self.comisionadosolicitud_foreign.solicitud_decreto_viaticos.montoviaticodiario_estrato_dos_interior
            elif estrato == 3:
                estrato_decreto = self.comisionadosolicitud_foreign.solicitud_decreto_viaticos.montoviaticodiario_estrato_tres_interior
            elif estrato == 4:
                estrato_decreto = self.comisionadosolicitud_foreign.solicitud_decreto_viaticos.montoviaticodiario_estrato_cuatro_interior
        
        return estrato_decreto
    
    def viaticos_computado(self):
        gabinete = self.comisionadosolicitud_nombre.comisionado_cargo.organigrama_cargo
        estrato = self.comisionadosolicitud_nombre.comisionado_cargo.organigrama_escalafon
        dias = self.comisionadosolicitud_foreign.cantidad_de_dias()
        if gabinete == "Vocal" or gabinete == "Presidente":
            estrato_decreto = 0
        else:
            if estrato == 1:
                estrato_decreto = self.comisionadosolicitud_foreign.solicitud_decreto_viaticos.montoviaticodiario_estrato_uno_interior
            elif estrato == 2:
                estrato_decreto = self.comisionadosolicitud_foreign.solicitud_decreto_viaticos.montoviaticodiario_estrato_dos_interior
            elif estrato == 3:
                estrato_decreto = self.comisionadosolicitud_foreign.solicitud_decreto_viaticos.montoviaticodiario_estrato_tres_interior
            elif estrato == 4:
                estrato_decreto = self.comisionadosolicitud_foreign.solicitud_decreto_viaticos.montoviaticodiario_estrato_cuatro_interior
        
        return dias * estrato_decreto
    
    def viaticos_total(self):
        total = self.viaticos_computado() + self.comisionadosolicitud_combustible + self.comisionadosolicitud_gastos
        return total

class Incorporacion(models.Model):
    class Meta:
        verbose_name = "Incorporación"
        verbose_name_plural = "Incorporaciones"
        constraints = [
            models.UniqueConstraint(
                fields=["incorporacion_solicitud"],
                name='unique_incorporacion_1'
            ),
        ]
    incorporacion_solicitud = models.ForeignKey("Solicitud", on_delete=models.CASCADE)
    incorporacion_actuacion = models.CharField("Actuación", max_length=18)
    incorporacion_solicitante = models.ForeignKey("Comisionado", on_delete=models.CASCADE) # Encargado del area solicitante
    incorporacion_resolucion = models.ForeignKey("InstrumentosLegalesResoluciones", verbose_name="Resolución Aprobada", on_delete=models.CASCADE)