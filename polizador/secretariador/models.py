from django.db import models
from simple_history.models import HistoricalRecords
from django.core.validators import MinValueValidator
from core.validators import FileValidator
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from django.db.models.functions import ExtractDay, Cast
from django.db.models.fields.generated import GeneratedField
from uuid_utils import compat


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
    if instance.instrumentolegalresoluciones_tipo == "D":
        filename = f"{instance.instrumentolegalresoluciones_numero}-{instance.instrumentolegalresoluciones_acta}-{instance.instrumentolegalresoluciones_ano}-{instance.instrumentolegalresoluciones_tipo}.pdf"
    else:
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

# WIP
# class Asuntos(models.Model):
#     class Meta:
#         verbose_name = "Asunto"
#         verbose_name_plural = "Asuntos"

#     asunto_nombre = models.CharField("Nombre", max_length=100)
#     asunto_descripcion = models.TextField("Descripción", max_length=600, default="")

#     def __str__(self):
#         return self.asunto_nombre
    
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
    instrumentolegalmemorandum_numero = models.PositiveIntegerField("Número")
    instrumentolegalmemorandum_ano = models.CharField("Año", max_length=5)
    instrumentolegalmemorandum_fecha_aprobacion = models.DateField("Fecha de Aprobación", default=timezone.now)
    instrumentolegalmemorandum_descripcion = models.CharField("Descripción", max_length=600, default="")
    instrumentolegalmemorandum = models.FileField(upload_to=generate_name_memorandum, max_length=500, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
    instrumentolegalmemorandum_str = GeneratedField(
        expression=ConcatOp(Cast('instrumentolegalmemorandum_numero', output_field=models.TextField()), models.Value(" - "), 'instrumentolegalmemorandum_ano', models.Value(" - "), 'instrumentolegalmemorandum_tipo'),
        output_field=models.TextField(),
        db_persist=True,
    )
    # Fields related to the automatic extraction of text from the digitalized instrument.
    instrumentolegalmemorandum_autocarga = models.BooleanField("Memorandum importado sin intervención humana.", default=False)
    instrumentolegalmemorandum_document = models.TextField("Texto Extraído por OCR", null=True, blank=True)
    instrumentolegalmemorandum_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    instrumentolegalmemorandum_history = HistoricalRecords()

    def __str__(self):
        return f"{self.get_instrumentolegalmemorandum_tipo_display()} Nº{self.instrumentolegalmemorandum_numero}/{self.instrumentolegalmemorandum_ano}"
    
    def get_absolute_url(self):
        if self.instrumentolegalmemorandum_tipo == "P":
            return reverse('secretariador:update-memorandum', kwargs={"pk": str(self.id)})
        elif self.instrumentolegalmemorandum_tipo == "D":
            return reverse('secretariador:update-memorandum', kwargs={"pk": str(self.id)})

class InstrumentosLegalesResoluciones(models.Model):
    class Meta:
        verbose_name = "Instrumento Legal(Resolución)"
        verbose_name_plural = "Instrumentos Legales(Resoluciones)"
        ordering = ["-instrumentolegalresoluciones_ano", "-instrumentolegalresoluciones_numero"]
        constraints = [
            models.UniqueConstraint(
                fields=["instrumentolegalresoluciones_tipo", "instrumentolegalresoluciones_numero", "instrumentolegalresoluciones_acta", "instrumentolegalresoluciones_ano"],
                name='unique_resolucion_1'
            ),
        ]

    TIPO = (
        ("P", "Resolución de Presidencia"),
        ("D", "Resolución de Directorio")
    )
    ESTADO_ESCANEO = (
        ("N", "Normal"),
        ("H", "Horrible"),
    )
    ACCION = (
        ("ADJ", "Adjudicatoria"),
        ("APR", "Aprobatoria"),
        ("RAT", "Ratificatoria"),
        ("AMP", "Ampliatoria"),
    )

    instrumentolegalresoluciones_tipo = models.CharField("Tipo", max_length=1, choices=TIPO, default="P")
    instrumentolegalresoluciones_numero = models.PositiveIntegerField("Número")
    instrumentolegalresoluciones_acta = models.CharField("Acta", max_length=3, default="")
    instrumentolegalresoluciones_ano = models.CharField("Año", max_length=5)
    instrumentolegalresoluciones_fecha_aprobacion = models.DateField("Fecha de Aprobación", default=timezone.now)
    instrumentolegalresoluciones_descripcion = models.CharField("Descripción", max_length=600, default="")
    instrumentolegalresoluciones_estado_escaneo = models.CharField("Estado del escaneo", max_length=1, choices=ESTADO_ESCANEO, default="N")
    instrumentolegalresoluciones_ad_referendum = models.BooleanField("Ad referendum", default=False)
    instrumentolegalresoluciones_accion = models.CharField("Acción", max_length=3, choices=ACCION, blank=True, null=True)
    instrumentolegalresoluciones = models.FileField(upload_to=generate_name_resoluciones, max_length=500, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
    instrumentolegalresoluciones_str = GeneratedField(
        expression=models.Case(
            models.When(
                instrumentolegalresoluciones_tipo="D",
                then=ConcatOp(Cast('instrumentolegalresoluciones_numero', output_field=models.TextField()), models.Value("-"), 'instrumentolegalresoluciones_acta', models.Value("-"), 'instrumentolegalresoluciones_ano'),
            ),
            default=ConcatOp(Cast('instrumentolegalresoluciones_numero', output_field=models.TextField()), models.Value("-"), 'instrumentolegalresoluciones_ano'),
            output_field=models.TextField(),
        ),
        output_field=models.TextField(),
        db_persist=True,
    )
    # Fields related to the automatic extraction of text from the digitalized resolution.
    instrumentolegalresoluciones_autocarga = models.BooleanField("Resolución importada sin intervención.", default=False)
    instrumentolegalresoluciones_document = models.TextField("Texto Extraído por OCR", null=True, blank=True)
    # Genera RES-yyyy-####-10-1 (Presidencia) o RES-yyyy-####-10-{acta} (Directorio)
    instrumentolegalresoluciones_numero_sgt = GeneratedField(
        expression=models.Case(
            models.When(
                instrumentolegalresoluciones_tipo="D",
                then=ConcatOp(models.Value("RES-"), "instrumentolegalresoluciones_ano", models.Value("-"), Cast("instrumentolegalresoluciones_numero", output_field=models.TextField()), models.Value("-10-"), "instrumentolegalresoluciones_acta"),
            ),
            default=ConcatOp(models.Value("RES-"), "instrumentolegalresoluciones_ano", models.Value("-"), Cast("instrumentolegalresoluciones_numero", output_field=models.TextField()), models.Value("-10-1")),
            output_field=models.CharField(max_length=25),
        ),
        output_field=models.CharField(max_length=25),
        db_persist=True,
    )
    instrumentolegalresoluciones_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    instrumentolegalresoluciones_history = HistoricalRecords()

    # WIP
    # # Fields related to data used in reports... Comisiones are not included due to the model having all the information needed.
    # instrumentolegalresoluciones_asunto = models.ForeignKey("Asuntos", on_delete=models.CASCADE, null=True, blank=True)
    # instrumentolegalresoluciones_empresa_beneficiaria = models.ForeignKey("carga.Empresa", on_delete=models.CASCADE, null=True, blank=True)
    # instrumentolegalresoluciones_agente_beneficiario = models.ForeignKey("Comisionado", on_delete=models.CASCADE, null=True, blank=True)
    # instrumentolegalresoluciones_monto = models.DecimalField("Monto", max_digits=12, decimal_places=2, default=0)
    # factura/boleta de pago y numero de comprobante

    def __str__(self):
        if self.instrumentolegalresoluciones_tipo == "D":
            return f"RES-{self.instrumentolegalresoluciones_ano}-{self.instrumentolegalresoluciones_numero}-10-{self.instrumentolegalresoluciones_acta}"
        return f"RES-{self.instrumentolegalresoluciones_ano}-{self.instrumentolegalresoluciones_numero}-10-1"

    def get_absolute_url(self):
        if self.instrumentolegalresoluciones_tipo == "P":
            return reverse('secretariador:update-resolucion-presidencia', kwargs={"pk": str(self.id)})
        elif self.instrumentolegalresoluciones_tipo == "D":
            return reverse('secretariador:update-resolucion-directorio', kwargs={"pk": str(self.id)})

class InstrumentosLegalesDecretos(models.Model):
    class Meta:
        verbose_name = "Instrumento Legal(Decreto)"
        verbose_name_plural = "Instrumentos Legales(Decretos)"
        ordering = ["-instrumentolegaldecretos_ano", "-instrumentolegaldecretos_numero"]
        constraints = [
            models.UniqueConstraint(
                fields=["instrumentolegaldecretos_tipo", "instrumentolegaldecretos_numero", "instrumentolegaldecretos_ano", "instrumentolegaldecretos_fecha_aprobacion"],
                name='unique_decretos_1'
            ),
        ]
        get_latest_by = ["instrumentolegaldecretos_ano", "instrumentolegaldecretos_numero"]

    TIPO = (
        ("N", "Decreto Nacional"),
        ("P", "Decreto Provincial")
    )

    instrumentolegaldecretos_tipo = models.CharField("Tipo", max_length=1, choices=TIPO, default="P")
    instrumentolegaldecretos_numero = models.PositiveIntegerField("Número")
    instrumentolegaldecretos_ano = models.CharField("Año", max_length=5)
    instrumentolegaldecretos_fecha_aprobacion = models.DateField("Fecha de Aprobación", default=timezone.now)
    instrumentolegaldecretos_descripcion = models.CharField("Descripción", max_length=600, default="Escala de viáticos")
    instrumentolegaldecretos = models.FileField(upload_to=generate_name_decretos, max_length=500, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf"))], null=True, blank=True)
    instrumentolegaldecretos_str = GeneratedField(
        expression=ConcatOp(Cast('instrumentolegaldecretos_numero', output_field=models.TextField()), models.Value(" - "), 'instrumentolegaldecretos_ano', models.Value(" - "), 'instrumentolegaldecretos_tipo'),
        output_field=models.TextField(),
        db_persist=True,
    )
    instrumentolegaldecretos_establece_licencia_anual = models.BooleanField(
        "Establece Licencia Anual",
        default=False,
        help_text="Tildado automáticamente si el decreto establece un período de Licencia Anual "
                   "Ordinaria. Se usa para acotar el desplegable de decretos al cargar una "
                   "Licencia/Permiso de tipo 'Anual'.",
    )
    instrumentolegaldecretos_establece_licencia_invierno = models.BooleanField(
        "Establece Licencia de Invierno",
        default=False,
        help_text="Tildado automáticamente si el decreto establece un período de Licencia Anual "
                   "de Invierno. Se usa para acotar el desplegable de decretos al cargar una "
                   "Licencia/Permiso de tipo 'Anual de Invierno'.",
    )
    instrumentolegaldecretos_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    instrumentolegaldecretos_history = HistoricalRecords()

    def __str__(self):
        return f"{self.get_instrumentolegaldecretos_tipo_display()} Nº{self.instrumentolegaldecretos_numero}/{self.instrumentolegaldecretos_ano}"
    
    def get_absolute_url(self):
        if self.montoviaticodiario_set.all():
            return reverse('secretariador:update-montoviaticodiario', kwargs={"pk": str(self.id)})
        else:    
            if self.instrumentolegaldecretos_tipo == "N":
                return reverse('secretariador:update-decreto', kwargs={"pk": str(self.id)})
            elif self.instrumentolegaldecretos_tipo == "P":
                return reverse('secretariador:update-decreto', kwargs={"pk": str(self.id)})

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
    montoviaticodiario_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    montoviaticodiario_history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.montoviaticodiario_decreto_reglamentario}"

ESCALAFON_CHOICES = (
    (1, "I"),
    (2, "II"),
    (3, "III"),
    (4, "IV"),
)

class ReglasViatico(models.Model):
    class Meta:
        verbose_name = "Reglas de Cálculo de Viáticos"
        verbose_name_plural = "Reglas de Cálculo de Viáticos"

    reglas_gabinete_cobra_viatico = models.BooleanField("Personal de gabinete cobra viático", default=False)
    reglas_autoridades_cobra_viatico_chaco = models.BooleanField("Autoridades (Directorio) cobran viático dentro de Chaco", default=False)
    reglas_autoridades_escalafon = models.PositiveSmallIntegerField("Escalafón de autoridades (Directorio)", choices=ESCALAFON_CHOICES, default=4)
    reglas_escalafon_unico_habilitado = models.BooleanField("Forzar un único escalafón para todos", default=False)
    reglas_escalafon_unico_valor = models.PositiveSmallIntegerField("Escalafón único", choices=ESCALAFON_CHOICES, default=2)
    reglas_externos_cobra_viatico = models.BooleanField("Comisionados externos cobran viático", default=True)
    reglas_escalafon_default_externos = models.PositiveSmallIntegerField("Escalafón por defecto para comisionados externos", choices=ESCALAFON_CHOICES, default=2)
    reglas_history = HistoricalRecords()

    def __str__(self):
        return "Reglas de Cálculo de Viáticos"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class Organigrama(models.Model):
    class Meta:
        verbose_name = "Organigrama"
        verbose_name_plural = "Organigramas"
    
    organigrama_cargo = models.CharField("Cargo", max_length=120)
    organigrama_escalafon = models.DecimalField("Escalafón", max_digits=1, decimal_places=0, default=2)
    organigrama_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    organigrama_history = HistoricalRecords()

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
    vehiculo_titular_agente = models.ForeignKey("personalizador.Agente", on_delete=models.CASCADE, null=True, blank=True)
    vehiculo_titular_empresa = models.ForeignKey("carga.Empresa", on_delete=models.CASCADE, null=True, blank=True)
    vehiculo_n_motor = models.CharField("Número de Motor", max_length=100, null=True, blank=True)
    vehiculo_n_chasis = models.CharField("Número de Chasis", max_length=100, null=True, blank=True)
    vehiculo_modelo_ano = models.DecimalField("Año del Modelo", max_digits=4, decimal_places=0, null=True, blank=True)
    vehiculo_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    vehiculo_history = HistoricalRecords()

    def __str__(self):
        return f"{self.vehiculo_modelo} - {self.vehiculo_patente}"
    
    def save(self, *args, **kwargs):
        self.vehiculo_patente = self.vehiculo_patente.replace(" ", "")
        super(Vehiculo, self).save(*args, **kwargs)

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
                fields=["solicitud_actuacion_jurisdiccion", "solicitud_actuacion_ano", "solicitud_actuacion_numero"],
                name="unique_solicitud_2"
            )
        ]
        
    solicitud_actuacion = GeneratedField(
        expression=ConcatOp('solicitud_actuacion_jurisdiccion', models.Value("-"), 'solicitud_actuacion_ano', models.Value("-"), 'solicitud_actuacion_numero', models.Value("-AE")),
        output_field=models.TextField(),
        db_persist=True,
    )
    solicitud_actuacion_jurisdiccion = models.CharField("Jurisdicción", max_length=3, default="E10")
    solicitud_actuacion_numero = models.DecimalField("N° Actuación", max_digits=6, decimal_places=0, validators=[MinValueValidator(0)], default=0, help_text="Solo el número de la actuación. Sin prefijo, sufijo o Año.")
    solicitud_actuacion_ano = models.DecimalField("Año Actuación", max_digits=4, decimal_places=0, validators=[MinValueValidator(0)], default=int(timezone.now().year))
    solicitud_solicitante = models.ForeignKey("personalizador.Agente", on_delete=models.CASCADE) # Encargado del area solicitante
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
    solicitud_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    solicitud_texto_actuacion = models.JSONField("Texto de la Resolución", null=True, blank=True, help_text="Texto de los considerandos y artículos editado desde la web para la generación del documento. Si está vacío, se genera automáticamente.")
    solicitud_history = HistoricalRecords()
    
    def solicitud_fechas(self):
        fechas = [self.solicitud_fecha_desde+timedelta(days=x) for x in range((self.solicitud_fecha_hasta-self.solicitud_fecha_desde).days+1)]
        fechas = [datetime.strftime(fecha, "%d/%m/%Y") for fecha in fechas]
        return fechas

    def get_comisionados(self):
        serialized_q = self.comisionadosolicitud_set.values_list("comisionadosolicitud_nombre__agente_nombreyapellido", flat=True)
        return list(serialized_q)

    def __str__(self):
        return f"{self.solicitud_actuacion}"

    def lista_localidades(self):
        return ", ".join(str(localidad) for localidad in self.solicitud_localidades.all())
    def lista_comisionados(self):
        return ", ".join(str(comisionado) for comisionado in self.comisionadosolicitud_set.all())
    
    def get_absolute_url(self):
        if self.solicitud_provincia.provincia_nombre == "Chaco":
            return reverse('secretariador:update-solicitud', kwargs={"pk": str(self.id)})
        else:
            return reverse('secretariador:update-solicitud-exterior', kwargs={"pk": str(self.id)})

class ComisionadoSolicitud(models.Model):
    class Meta:
        verbose_name = "Comisionado Solicitud"
        verbose_name_plural = "Comisionado Solicitudes"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(comisionadosolicitud_nombre__isnull=False, comisionadosolicitud_externo__isnull=True)
                    | models.Q(comisionadosolicitud_nombre__isnull=True, comisionadosolicitud_externo__isnull=False)
                ),
                name="comisionadosolicitud_agente_xor_externo",
            ),
        ]

    comisionadosolicitud_foreign = models.ForeignKey("Solicitud", on_delete=models.CASCADE, null=True, blank=True)
    comisionadosolicitud_incorporacion_foreign = models.ForeignKey("Incorporacion", on_delete=models.CASCADE, null=True, blank=True)
    comisionadosolicitud_nombre = models.ForeignKey("personalizador.Agente", on_delete=models.CASCADE, null=True, blank=True, help_text="Agente del organismo. Exactamente uno de Agente/Externo debe estar cargado.")
    comisionadosolicitud_externo = models.ForeignKey("personalizador.ComisionadoExterno", on_delete=models.CASCADE, null=True, blank=True, help_text="Persona externa al organismo. Exactamente uno de Agente/Externo debe estar cargado.")
    comisionadosolicitud_colaborador = models.BooleanField("Colab.?")
    comisionadosolicitud_chofer = models.BooleanField("Chofer?")
    comisionadosolicitud_combustible = models.DecimalField("Combustible", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    comisionadosolicitud_pasaje = models.DecimalField("Pasajes", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    comisionadosolicitud_gastos = models.DecimalField("Gastos", max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    comisionadosolicitud_sin_viatico = models.BooleanField("$0", default=False)
    comisionadosolicitud_viatico_diario = models.DecimalField("Viatico Diario", max_digits=12, decimal_places=2, default=0, editable=False, null=True, blank=True) # Field is editable=False because it is calculated in the clean method.
    comisionadosolicitud_viatico_computado = models.DecimalField("Viatico Computado", max_digits=12, decimal_places=2, default=0, editable=False, null=True, blank=True) # Field is editable=False because it is calculated in the clean method.
    comisionadosolicitud_viatico_total = models.DecimalField("Viatico Total", max_digits=12, decimal_places=2, default=0, editable=False, null=True, blank=True) # Field is editable=False because it is calculated in the clean method.
    comisionadosolicitud_cantidad_de_dias = models.DurationField("Días", editable=False, null=True, blank=True)
    comisionadosolicitud_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    comisionadosolicitud_history = HistoricalRecords()

    def get_origin(self):
        return self.comisionadosolicitud_foreign if self.comisionadosolicitud_foreign is not None else self.comisionadosolicitud_incorporacion_foreign.incorporacion_solicitud

    @property
    def persona(self):
        """Devuelve el Agente o el ComisionadoExterno cargado, sea cual sea
        (son mutuamente excluyentes, ver constraint `comisionadosolicitud_agente_xor_externo`).
        Ambos exponen los mismos atributos (`agente_nombres`, `agente_apellidos`,
        `agente_nombreyapellido`, `abreviatura`, `dni`, `cuil`, `sexo`), así que
        el resto del código puede leer `comisionado.persona.<attr>` sin
        importar de qué tipo es."""
        return self.comisionadosolicitud_nombre or self.comisionadosolicitud_externo

    def __str__(self):
        """
        Returns a string representation of the object.
        The string representation consists of the foreign key value, which is either the value of `comisionadosolicitud_foreign` or `comisionadosolicitud_incorporacion_foreign`,
        followed by the last name and first name of the commissioned person (Agente or ComisionadoExterno).

        Returns:
            str: A string representation of the object.
        """
        foreign = self.get_origin()
        persona = self.persona
        return f"{foreign} - {persona.agente_apellidos}, {persona.agente_nombres}"

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
        if not self.comisionadosolicitud_nombre and not self.comisionadosolicitud_externo:
            raise ValidationError("Debe cargarse un agente del organismo o una persona externa.")
        if self.comisionadosolicitud_nombre and self.comisionadosolicitud_externo:
            raise ValidationError("No se puede cargar un agente del organismo y una persona externa al mismo tiempo.")

    def valor_viatico_dia(self):
        """
        Calculates the daily viatic value based on the escalafón of the commissioned
        person and the rules configured in ReglasViatico.

        Returns:
            float: The daily viatic value. Returns 0 if excepted by ReglasViatico or
            by comisionadosolicitud_colaborador/comisionadosolicitud_sin_viatico.
        """
        if self.comisionadosolicitud_colaborador or self.comisionadosolicitud_sin_viatico:
            return 0

        foreign = self.get_origin()
        decreto = foreign.solicitud_decreto_viaticos
        es_chaco = foreign.solicitud_provincia.provincia_nombre == "Chaco"
        reglas = ReglasViatico.get_solo()

        # Los chequeos de directorio/gabinete solo aplican a agentes del
        # organismo; un comisionado externo tiene su propia excepción
        # (reglas_externos_cobra_viatico).
        es_autoridad = False
        if self.comisionadosolicitud_nombre is not None:
            agente = self.comisionadosolicitud_nombre
            es_autoridad = agente.directorio_set.exists()
            if agente.agente_personal_de_gabinete and not reglas.reglas_gabinete_cobra_viatico:
                return 0
            if es_autoridad and es_chaco and not reglas.reglas_autoridades_cobra_viatico_chaco:
                return 0
        elif not reglas.reglas_externos_cobra_viatico:
            return 0

        if reglas.reglas_escalafon_unico_habilitado:
            estrato = reglas.reglas_escalafon_unico_valor
        elif self.comisionadosolicitud_nombre is not None:
            estrato = reglas.reglas_autoridades_escalafon if es_autoridad else self.comisionadosolicitud_nombre.agente_escalafon
        else:
            estrato = reglas.reglas_escalafon_default_externos

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
                fields=["incorporacion_actuacion_jurisdiccion","incorporacion_actuacion_ano", "incorporacion_actuacion_numero"],	
                name="unique_incorporacion_2"
            ),
        ]
        
    incorporacion_solicitud = models.ForeignKey("Solicitud", help_text="Actuación a la que se incorpora los agentes.", on_delete=models.CASCADE)
    incorporacion_actuacion = GeneratedField(
        expression=ConcatOp("incorporacion_actuacion_jurisdiccion", models.Value("-"), 'incorporacion_actuacion_ano', models.Value("-"), 'incorporacion_actuacion_numero', models.Value("-AE")),
        output_field=models.TextField(),
        db_persist=True,
    )
    incorporacion_actuacion_jurisdiccion = models.CharField("Jurisdicción", max_length=3, default="E10")
    incorporacion_actuacion_numero = models.DecimalField("N° Actuación", max_digits=6, decimal_places=0, validators=[MinValueValidator(0)], default=0, help_text="Solo el número de la actuación. Sin prefijo, sufijo o Año.")
    incorporacion_actuacion_ano = models.DecimalField("Año Actuación", max_digits=4, decimal_places=0, validators=[MinValueValidator(0)], default=int(timezone.now().year))
    incorporacion_solicitante = models.ForeignKey("personalizador.Agente", on_delete=models.CASCADE) # Encargado del area solicitante
    incorporacion_resolucion = models.ForeignKey("InstrumentosLegalesResoluciones", verbose_name="Resolución Aprobada", help_text="Resolución que aprueba la incorporación de los agentes.", on_delete=models.CASCADE, blank=True, null=True)
    incorporacion_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    incorporacion_texto_actuacion = models.JSONField("Texto de la Resolución", null=True, blank=True, help_text="Texto de los considerandos y artículos editado desde la web para la generación del documento. Si está vacío, se genera automáticamente.")
    incorporacion_history = HistoricalRecords()

    def __str__(self):
        return f"{self.incorporacion_actuacion}"
    
    def cantidad_de_dias(self):
        return self.incorporacion_solicitud.solicitud_cantidad_de_dias
    
    def get_absolute_url(self):
        return reverse("secretariador:update-incorporacion", kwargs={"pk": str(self.id)})

class EncabezadoDocumento(models.Model):
    class Meta:
        verbose_name = "Encabezado de Documento"
        verbose_name_plural = "Encabezados de Documento"
        ordering = ["-encabezadodocumento_creado"]
        get_latest_by = ["encabezadodocumento_creado"]

    encabezadodocumento_archivo = models.FileField(
        "Archivo (.docx)",
        upload_to="encabezados/",
        max_length=500,
        validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ))],
    )
    encabezadodocumento_creado = models.DateTimeField(auto_now_add=True)
    encabezadodocumento_subido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    encabezadodocumento_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    encabezadodocumento_history = HistoricalRecords()

    def __str__(self):
        return f"Encabezado del {self.encabezadodocumento_creado:%d/%m/%Y %H:%M}"

    @classmethod
    def vigente(cls):
        """Devuelve el encabezado subido más recientemente, o None si nunca se subió uno."""
        return cls.objects.order_by("-encabezadodocumento_creado").first()
