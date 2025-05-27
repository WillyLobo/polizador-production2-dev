from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from secretariador.functions import FileValidator, CuitValidator
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
import os
from django.db.models.functions import ExtractDay
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
def generate_name_memorandum(instance, filename):
    """
    Generates a name for a memorandum file based on the given instance and filename.

    Parameters:
        instance (object): The instance of the resolution.
        filename (str): The original filename of the resolution.

    Returns:
        str: The generated name for the resolution file.
    """
    directorio = "instrumentoslegales/memorandum/"
    filename = f"{instance.instrumentolegalmemorandum_numero}-{instance.instrumentolegalmemorandum_ano}-{instance.instrumentolegalmemorandum_tipo}.pdf"
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
class InstrumentosLegalesMemorandum(models.Model):
    class Meta:
        verbose_name = "Instrumento Legal(Memorandum)"
        verbose_name_plural = "Instrumentos Legales(Memorandums)"
        ordering = ["-instrumentolegalmemorandum_ano", "-instrumentolegalmemorandum_numero"]
        constraints = [
            models.UniqueConstraint(
                fields=["instrumentolegalmemorandum_tipo", "instrumentolegalmemorandum_numero", "instrumentolegalmemorandum_ano"],
                name='unique_memorandum_1'
            ),
        ]

    TIPO = (
        ("P", "Presidencia"),
        ("D", "Dirección General de Gestión Administrativa")
    )

    instrumentolegalmemorandum_tipo = models.CharField("Tipo", max_length=1, choices=TIPO, default="P")
    instrumentolegalmemorandum_numero = models.CharField("Número", max_length=7)
    instrumentolegalmemorandum_ano = models.CharField("Año", max_length=5)
    instrumentolegalmemorandum_fecha_aprobacion = models.DateField("Fecha de Aprobación", default=timezone.now)
    instrumentolegalmemorandum_descripcion = models.CharField("Descripción", max_length=600, default="")
    instrumentolegalmemorandum = models.FileField(upload_to=generate_name_memorandum, max_length=500, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
    instrumentolegalmemorandum_str = GeneratedField(
        expression=ConcatOp('instrumentolegalmemorandum_numero', models.Value(" - "), 'instrumentolegalmemorandum_ano', models.Value(" - "), 'instrumentolegalmemorandum_tipo'),
        output_field=models.TextField(),
        db_persist=True,
    )
    # Fields related to the automatic extraction of text from the digitalized instrument.
    instrumentolegalmemorandum_autocarga = models.BooleanField("Memorandum importado sin intervención humana.", default=False)
    instrumentolegalmemorandum_document = models.TextField("Texto Extraído por OCR", null=True, blank=True)

    def __str__(self):
        return f"{self.get_instrumentolegalmemorandum_tipo_display()} Nº{self.instrumentolegalmemorandum_numero}/{self.instrumentolegalmemorandum_ano}"
    
class InstrumentosLegalesResoluciones(models.Model):
    class Meta:
        verbose_name = "Instrumento Legal(Resolución)"
        verbose_name_plural = "Instrumentos Legales(Resoluciones)"
        ordering = ["-instrumentolegalresoluciones_ano", "-instrumentolegalresoluciones_numero"]
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
    instrumentolegalresoluciones_acta = models.CharField("Acta", max_length=3, default="")
    instrumentolegalresoluciones_ano = models.CharField("Año", max_length=5)
    instrumentolegalresoluciones_fecha_aprobacion = models.DateField("Fecha de Aprobación", default=timezone.now)
    instrumentolegalresoluciones_descripcion = models.CharField("Descripción", max_length=600, default="")
    instrumentolegalresoluciones = models.FileField(upload_to=generate_name_resoluciones, max_length=500, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
    instrumentolegalresoluciones_str = GeneratedField(
        expression=ConcatOp('instrumentolegalresoluciones_numero', models.Value(" - "), 'instrumentolegalresoluciones_ano', models.Value(" - "), 'instrumentolegalresoluciones_tipo'),
        output_field=models.TextField(),
        db_persist=True,
    )
    # Fields related to the automatic extraction of text from the digitalized resolution.
    instrumentolegalresoluciones_autocarga = models.BooleanField("Resolución importada sin intervención.", default=False)
    instrumentolegalresoluciones_document = models.TextField("Texto Extraído por OCR", null=True, blank=True)

    def __str__(self):
        return f"{self.get_instrumentolegalresoluciones_tipo_display()} Nº{self.instrumentolegalresoluciones_numero}/{self.instrumentolegalresoluciones_ano}"

class InstrumentosLegalesDecretos(models.Model):
    class Meta:
        verbose_name = "Instrumento Legal(Decreto)"
        verbose_name_plural = "Instrumentos Legales(Decretos)"
        ordering = ["-instrumentolegaldecretos_ano", "-instrumentolegaldecretos_numero"]
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
    instrumentolegaldecretos = models.FileField(upload_to=generate_name_decretos, max_length=500, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
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
        ordering = ["montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_ano", "montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_numero"]
        get_latest_by = ["montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_ano", "montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_numero"]
    
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
        constraints = [
            models.UniqueConstraint(
                fields=["comisionado_nombres", "comisionado_apellidos", "comisionado_dni"],
                name='unique_comisionado_1'
            ),
        ]
    SEXO = (
        ("M", "Masculino"),
        ("F", "Femenino")
    )

    comisionado_nombres = models.CharField("Nombres", max_length=120)
    comisionado_apellidos = models.CharField("Apellidos", max_length=120)
    comisionado_abreviatura = models.CharField("Abreviatura", max_length=10, help_text="(Sr., Sra., Dr., Dra., Etc.)")
    comisionado_sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    comisionado_cargo = models.ForeignKey("Organigrama", on_delete=models.CASCADE)
    comisionado_cargo_decreto = models.ForeignKey("personalizador.Cargos", verbose_name="Cargo Decreto", related_name="cargo_decreto", on_delete=models.CASCADE, null=True, blank=True)
    comisionado_cargo_interno = models.ForeignKey("personalizador.Cargos", verbose_name="Cargo Interno", related_name="cargo_interno", on_delete=models.CASCADE, null=True, blank=True)
    comisionado_cargo_interno_resolucion = models.ForeignKey("InstrumentosLegalesResoluciones", on_delete=models.CASCADE, null=True, blank=True)
    comisionado_dni = models.DecimalField("DNI:", max_digits=9, decimal_places=0, validators=[MinValueValidator(0)], unique=True)
    comisionado_cuit = models.CharField("CUIT", max_length=13, validators=[CuitValidator()])
    comisionado_nombreyapellido = GeneratedField(
        expression=ConcatOp('comisionado_apellidos', models.Value(", "), 'comisionado_nombres'),
        output_field=models.TextField(),
        db_persist=True,
    )
    comisionado_verificado_contra_padron = models.BooleanField("Chequeado",default=False)
    comisionado_personal_transitorio = models.BooleanField("Personal Transitorio",default=False)
    comisionado_personal_de_gabinete = models.BooleanField("Personal de Gabinete",default=False)

    def __str__(self):
        if self.comisionado_personal_transitorio:
            return f"(C){self.comisionado_apellidos}, {self.comisionado_nombres} - DNI Nº{self.comisionado_dni}"
        else:
            return f"{self.comisionado_apellidos}, {self.comisionado_nombres} - DNI Nº{self.comisionado_dni}"
    
    def nombreydni(self):
        return f"{self.comisionado_abreviatura} {self.comisionado_apellidos}, {self.comisionado_nombres}-DNI Nº{self.comisionado_dni}"

    def comisionado_nombre(self):
        return f"{self.comisionado_apellidos}, {self.comisionado_nombres}"

class Organigrama(models.Model):
    class Meta:
        verbose_name = "Organigrama"
        verbose_name_plural = "Organigramas"
    
    organigrama_cargo = models.CharField("Cargo", max_length=120)
    organigrama_escalafon = models.DecimalField("Escalafón", max_digits=1, decimal_places=0, default=2)

    def __str__(self):
        return self.organigrama_cargo

class Vehiculo(models.Model):
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        constraints = [
            models.UniqueConstraint(
                fields=["vehiculo_modelo", "vehiculo_patente"],
                name='unique_vehiculo_1'
            ),
        ]
        ordering = ["vehiculo_modelo", "vehiculo_patente"]
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
    vehiculo_titular_agente = models.ForeignKey("Comisionado", on_delete=models.CASCADE, null=True, blank=True)
    vehiculo_titular_empresa = models.ForeignKey("carga.Empresa", on_delete=models.CASCADE, null=True, blank=True)
    vehiculo_n_motor = models.CharField("Número de Motor", max_length=100, null=True, blank=True)
    vehiculo_n_chasis = models.CharField("Número de Chasis", max_length=100, null=True, blank=True)
    vehiculo_modelo_ano = models.DecimalField("Año del Modelo", max_digits=4, decimal_places=0, null=True, blank=True)

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
            models.UniqueConstraint(
                fields=["solicitud_actuacion_ano", "solicitud_actuacion_numero"],
                name="unique_solicitud_2"
            )
        ]
        
    solicitud_actuacion = GeneratedField(
        expression=ConcatOp(models.Value("E10-"), 'solicitud_actuacion_ano', models.Value("-"), 'solicitud_actuacion_numero', models.Value("-AE")),
        output_field=models.TextField(),
        db_persist=True,
    )
    solicitud_actuacion_jurisdiccion = models.CharField("Jurisdicción", max_length=3, default="E10")
    solicitud_actuacion_numero = models.DecimalField("N° Actuación", max_digits=6, decimal_places=0, validators=[MinValueValidator(0)], default=0, help_text="Solo el número de la actuación. Sin prefijo, sufijo o Año.")
    solicitud_actuacion_ano = models.DecimalField("Año Actuación", max_digits=4, decimal_places=0, validators=[MinValueValidator(0)], default=int(timezone.now().year))
    solicitud_solicitante = models.ForeignKey("Comisionado", on_delete=models.CASCADE) # Encargado del area solicitante
    solicitud_provincia = models.ForeignKey("carga.Provincia", on_delete=models.CASCADE)
    solicitud_localidades = models.ManyToManyField("carga.Localidad", blank=True)
    solicitud_ciudad = models.CharField("Ciudad", help_text="... en la ciudad de #Texto ingresado en el formulario#", max_length=200, blank=True, null=True)
    solicitud_decreto_viaticos = models.ForeignKey("MontoViaticoDiario", on_delete=models.CASCADE)
    solicitud_fecha_desde = models.DateField("Fecha Inicio")
    solicitud_fecha_hasta = models.DateField("Fecha Regreso")
    solicitud_tareas = models.TextField("Tareas a Realizar", help_text="... a fin de #Texto ingresado en el formulario# en la localidad de #Localidad#")
    solicitud_vehiculo = models.ForeignKey("Vehiculo", on_delete=models.CASCADE, blank=True, null=True)
    solicitud_aereo = models.BooleanField("Aereo", help_text="Tildar si es viaje aereo", blank=True, null=True)
    solicitud_dia_inhabil = models.BooleanField("Dia Inhábil", help_text="Tildar si es un diá de no laboral")
    solicitud_resolucion = models.ForeignKey("InstrumentosLegalesResoluciones", verbose_name="Resolución Aprobada", on_delete=models.CASCADE, blank=True, null=True)
    solicitud_cantidad_de_dias = GeneratedField(
        expression=models.F('solicitud_fecha_hasta') - models.F('solicitud_fecha_desde') + timedelta(days=1),
        output_field=models.DurationField(),
        db_persist=True
    )
    solicitud_anulada = models.BooleanField("Anulada", default=False, help_text="Si la solicitud se encuentra anulada, no se registra en los reportes.")
    
    def solicitud_fechas(self):
        fechas = [self.solicitud_fecha_desde+timedelta(days=x) for x in range((self.solicitud_fecha_hasta-self.solicitud_fecha_desde).days+1)]
        fechas = [datetime.strftime(fecha, "%d/%m/%Y") for fecha in fechas]
        return fechas

    def get_comisionados(self):
        serialized_q = self.comisionadosolicitud_set.values_list("comisionadosolicitud_nombre__comisionado_nombreyapellido", flat=True)
        return list(serialized_q)

    def __str__(self):
        return f"{self.solicitud_actuacion}"
    
    def get_absolute_url(self):
        return reverse('secretariador:update-solicitud', kwargs={"pk": str(self.id)})

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
    comisionadosolicitud_pasaje = models.DecimalField("Pasajes", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    comisionadosolicitud_gastos = models.DecimalField("Gastos", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    comisionadosolicitud_sin_viatico = models.BooleanField("Sin viático", default=False)
    comisionadosolicitud_viatico_diario = models.DecimalField("Viatico Diario", max_digits=12, decimal_places=2, default=0, editable=False, null=True, blank=True) # Field is editable=False because it is calculated in the clean method.
    comisionadosolicitud_viatico_computado = models.DecimalField("Viatico Computado", max_digits=12, decimal_places=2, default=0, editable=False, null=True, blank=True) # Field is editable=False because it is calculated in the clean method.
    comisionadosolicitud_viatico_total = models.DecimalField("Viatico Total", max_digits=12, decimal_places=2, default=0, editable=False, null=True, blank=True) # Field is editable=False because it is calculated in the clean method.
    comisionadosolicitud_cantidad_de_dias = models.DurationField("Días", editable=False, null=True, blank=True)

    def get_origin(self):
        return self.comisionadosolicitud_foreign if self.comisionadosolicitud_foreign is not None else self.comisionadosolicitud_incorporacion_foreign.incorporacion_solicitud
    
    def __str__(self):
        """
        Returns a string representation of the object.
        The string representation consists of the foreign key value, which is either the value of `comisionadosolicitud_foreign` or `comisionadosolicitud_incorporacion_foreign`,
        followed by the last name and first name of the `comisionadosolicitud_nombre` object.

        Returns:
            str: A string representation of the object.
        """
        foreign = self.get_origin()
        return f"{foreign} - {self.comisionadosolicitud_nombre.comisionado_apellidos}, {self.comisionadosolicitud_nombre.comisionado_nombres}"
    
    def clean(self):
        """
        Sets the `comisionadosolicitud_combustible`, `comisionadosolicitud_pasaje` and `comisionadosolicitud_gastos` fields to 0 if they are None, otherwise keeps their current values.
        This function is used to ensure that these fields are always set to a non-null value. It is typically called during the cleaning process of a form or model instance.
        Returns:
            None
        """
        self.comisionadosolicitud_gastos = 0 if self.comisionadosolicitud_gastos is None else self.comisionadosolicitud_gastos
        self.comisionadosolicitud_pasaje = 0 if self.comisionadosolicitud_pasaje is None else self.comisionadosolicitud_pasaje
        self.comisionadosolicitud_combustible = 0 if self.comisionadosolicitud_combustible is None else self.comisionadosolicitud_combustible

    def valor_viatico_dia(self):
        """
        Calculates the daily viatic value based on the position and stratum of the commissioned person.

        Returns:
            float: The daily viatic value. Returns 0 if the position is "Vocal" or "Presidente".
        """
        foreign = self.get_origin()
        gabinete = self.comisionadosolicitud_nombre.comisionado_cargo.organigrama_cargo
        estrato = self.comisionadosolicitud_nombre.comisionado_cargo.organigrama_escalafon
        decreto = foreign.solicitud_decreto_viaticos
        es_chaco = foreign.solicitud_provincia.provincia_nombre == "Chaco"

        if gabinete in ["Vocal", "Presidente"]:
            return 0 if es_chaco else decreto.montoviaticodiario_estrato_cuatro_exterior
        
        if self.comisionadosolicitud_colaborador:
            return 0
        
        if self.comisionadosolicitud_sin_viatico:
            return 0
        
        if es_chaco:
            campo = f"montoviaticodiario_estrato_{['uno', 'dos', 'tres', 'cuatro'][int(estrato)-1]}_interior"
        else:
            campo = f"montoviaticodiario_estrato_{['uno', 'dos', 'tres', 'cuatro'][int(estrato)-1]}_exterior"
        
        return getattr(decreto, campo)
    
    def viaticos_computado(self):
        """
        Calculates the total amount of viaticos based on the position and stratum of the commissioned person.

        Returns:
            float: The total amount of viaticos computed.
        """
        dias = self.get_origin().solicitud_cantidad_de_dias
        estrato_decreto = self.valor_viatico_dia() 
        return int(dias.days) * estrato_decreto
    
    def viaticos_total(self):
        """
        Calculates the total amount of viaticos based on the computed viaticos, combustible, and gastos.

        Returns:
            float: The total amount of viaticos.
        """
        total = self.viaticos_computado() + self.comisionadosolicitud_combustible + self.comisionadosolicitud_gastos + self.comisionadosolicitud_pasaje
        return total
    
    def save(self, *args, **kwargs):
        self.comisionadosolicitud_cantidad_de_dias = self.get_origin().solicitud_cantidad_de_dias
        self.comisionadosolicitud_viatico_diario = self.valor_viatico_dia()
        self.comisionadosolicitud_viatico_computado = self.viaticos_computado()
        self.comisionadosolicitud_viatico_total = self.viaticos_total()
        super(ComisionadoSolicitud, self).save(*args, **kwargs)

class Incorporacion(models.Model):
    class Meta:
        verbose_name = "Incorporación"
        verbose_name_plural = "Incorporaciones"
        constraints = [
            models.UniqueConstraint(
                fields=["incorporacion_solicitud"],
                name='unique_incorporacion_1'
            ),
            models.UniqueConstraint(
                fields=["incorporacion_actuacion_ano", "incorporacion_actuacion_numero"],	
                name="unique_incorporacion_2"
            ),
        ]
        
    incorporacion_solicitud = models.ForeignKey("Solicitud", help_text="Actuación a la que se incorpora los agentes.", on_delete=models.CASCADE)
    incorporacion_actuacion = GeneratedField(
        expression=ConcatOp(models.Value("E10-"), 'incorporacion_actuacion_ano', models.Value("-"), 'incorporacion_actuacion_numero', models.Value("-AE")),
        output_field=models.TextField(),
        db_persist=True,
    )
    incorporacion_actuacion_numero = models.DecimalField("N° Actuación", max_digits=6, decimal_places=0, validators=[MinValueValidator(0)], default=0, help_text="Solo el número de la actuación. Sin prefijo, sufijo o Año.")
    incorporacion_actuacion_ano = models.DecimalField("Año Actuación", max_digits=4, decimal_places=0, validators=[MinValueValidator(0)], default=int(timezone.now().year))
    incorporacion_solicitante = models.ForeignKey("Comisionado", on_delete=models.CASCADE) # Encargado del area solicitante
    incorporacion_resolucion = models.ForeignKey("InstrumentosLegalesResoluciones", verbose_name="Resolución Aprobada", help_text="Resolución que aprueba la incorporación de los agentes.", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.incorporacion_actuacion}"
    
    def cantidad_de_dias(self):
        return self.incorporacion_solicitud.solicitud_cantidad_de_dias
    
    def get_absolute_url(self):
        return reverse("secretariador:update-incorporacion", kwargs={"pk": str(self.id)})
