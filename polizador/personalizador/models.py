from django.db import models
from simple_history.models import HistoricalRecords
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from secretariador.functions import FileValidator, CuitValidator
from datetime import datetime
from uuid_utils import compat

class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"

class CustomUser(AbstractUser):
    first_name = models.CharField("Nombre", max_length=128)
    last_name = models.CharField("Apellido", max_length=128)
    usuario_dni = models.DecimalField(
        "DNI:", max_digits=9, decimal_places=0,
         validators=[MinValueValidator(0)],
         unique=True,
         null=True,
         blank=True
         )
    usuario_history = HistoricalRecords()

class Agente(models.Model):
    class Meta:
        verbose_name = "Agente"
        verbose_name_plural = "Agentes"
        ordering = ("agente_apellidos","agente_nombres")

    agente_usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    agente_nombres = models.CharField("Nombres", max_length=120)
    agente_apellidos = models.CharField("Apellidos", max_length=120)
    agente_nombreyapellido = models.GeneratedField(
        expression=ConcatOp(models.F("agente_nombres"), models.Value(" "), models.F("agente_apellidos")),
        output_field=models.CharField("Nombre y Apellido", max_length=256, editable=False),
        db_persist=True
    )
    agente_apellidoynombre_coma = models.GeneratedField(
        expression=ConcatOp(models.F("agente_apellidos"), models.Value(", "), models.F("agente_nombres")),
        output_field=models.CharField("Apellido y Nombres", max_length=256, editable=False),
        db_persist=True
    )
    n_legajo = models.IntegerField("Numero de legajo", blank=True, null=True)
    # Datos Personales
    sexo = models.ForeignKey("GeneroAgente", on_delete=models.CASCADE)
    abreviatura = models.CharField("Abreviatura", max_length=10, blank=True, null=True)
    telefono = models.CharField("Telefono", max_length=20, blank=True, null=True)
    email = models.EmailField("Email", blank=True,null=True)
    titulo_profesional = models.ManyToManyField("TituloProfesional", blank=True)
    matricula = models.CharField("Matricula Profesional", max_length=10, blank=True, null=True)
    dni = models.DecimalField("DNI:", max_digits=9, decimal_places=0, unique=True, validators=[MinValueValidator(0)])
    cuil = models.CharField("CUIT", max_length=13, validators=[CuitValidator()])
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", blank=True, null=True)
    # Datos Dependencia
    fecha_ingreso = models.DateField("Fecha de Ingreso", blank=True, null=True)
    fecha_pase_a_planta = models.DateField("Fecha de pase a planta permanente", blank=True, null=True) # fecha utilizada para el computo de antiguedad.
    n_decreto = models.CharField(max_length=10, blank=True, null=True)
    n_resolucion_bonificacion = models.CharField(max_length=13, blank=True, null=True)
    porcentaje_bonificacion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    categoria = models.ForeignKey("Categoria", on_delete=models.CASCADE, blank=True, null=True)
    denominacion_cargo = models.ForeignKey("DenominacionCargo", related_name="agente_denominacion_cargo", on_delete=models.CASCADE, blank=True, null=True)
    cargo_interno = models.ForeignKey("DenominacionCargo", related_name="agente_cargo_interno", on_delete=models.CASCADE, blank=True, null=True)
    n_resolucion_cargo_interno = models.CharField(max_length=13, blank=True, null=True)
    apartado = models.ForeignKey("ApartadoCargo", on_delete=models.CASCADE, blank=True, null=True)
    ceic = models.ForeignKey("CEIC", on_delete=models.CASCADE, blank=True, null=True)
    grupo = models.ForeignKey("GrupoCargo", on_delete=models.CASCADE, blank=True, null=True)
    activdad_central = models.CharField(max_length=1, default="1")
    actividad_especifica = models.ForeignKey("ActividadEspecifica", on_delete=models.CASCADE, blank=True, null=True)
    oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE, blank=True, null=True)
    n_decreto_transferencia_definitiva = models.CharField(max_length=10, blank=True, null=True)
    domicilio_direccion = models.CharField(max_length=500, blank=True, null=True)
    domicilio_barrio = models.CharField(max_length=300, blank=True, null=True)
    domicilio_localidad = models.ForeignKey("carga.Localidad", on_delete=models.CASCADE, blank=True, null=True)
    # Campos calculados en base a lo que diga la fecha de la resolucion de aportes.
    # Extraer años, meses, dias para computar.
    aportes_ley_resolucion = models.CharField(max_length=13, blank=True, null=True)
    # aportes_ley = generatedfield(delta de fecha_desde a fecha_hasta)
    # aportes_anses = generatedfield(delta de anses_fecha_desde a anses_fecha_hasta)
    # años_totales = generatedfield(delta de fecha_de_igreso a hoy)
    # fecha_carga_interna = models.DateField("Fecha de inicio de aportes", blank=True, null=True)
    # FLAGS
    agente_verificado_contra_padron = models.BooleanField("Chequeado",default=False)
    agente_es_inpector_obra = models.BooleanField("Inspector de Obra",default=False)
    agente_personal_transitorio = models.BooleanField("Personal Transitorio",default=False)
    agente_personal_de_gabinete = models.BooleanField("Personal de Gabinete",default=False)
    # Otros
    agente_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    agente_history = HistoricalRecords()

    @property
    def edad(self):
        return int((datetime.now().year - self.fecha_nacimiento.year))

    def __str__(self):
        if self.agente_personal_transitorio:
            return f"(C){self.agente_nombreyapellido} - DNI Nº{self.dni}"
        else:
            return f"{self.agente_nombreyapellido} - DNI Nº{self.dni}"

class GeneroAgente(models.Model):
    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

    generoagente_nombre = models.CharField(max_length=20, unique=True)
    generoagente_history = HistoricalRecords()

    def __str__(self):
        return self.generoagente_nombre

class TituloProfesional(models.Model):
    class Meta:
        verbose_name = "Título Profesional"
        verbose_name_plural = "Títulos Profesionales"
   
    tituloprofesional_nombre = models.CharField(max_length=200)
    tituloprofesional_grado = models.CharField(max_length=50, help_text="Grado académico del título, ej: Universitario, Terciario, etc.")
    tituloprofesional_history = HistoricalRecords()

    def __str__(self):
        return self.tituloprofesional_nombre

class Categoria(models.Model):
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    categoria_codigo = models.DecimalField(max_digits=2, decimal_places=0)
    categoria_nombre = models.CharField(max_length=100)
    categoria_history = HistoricalRecords()

    def __str__(self):
        return self.categoria_nombre

class DenominacionCargo(models.Model):
    class Meta:
        verbose_name = "Denominación de Cargo"
        verbose_name_plural = "Denominaciones de Cargos"

    denominacion = models.CharField(max_length=100)
    denominacioncargo_history = HistoricalRecords()

    def __str__(self):
        return self.denominacion

class ApartadoCargo(models.Model):
    class Meta:
        verbose_name = "Apartado"
        verbose_name_plural = "Apartados"

    apartadocargo_denominacion = models.CharField(max_length=1, unique=True)
    apartadocargo_history = HistoricalRecords()

    def __str__(self):
        return self.apartadocargo_denominacion

class CEIC(models.Model):
    class Meta:
        verbose_name = "CEIC"
        verbose_name_plural = "CEIC"

    ceic = models.CharField(max_length=10, unique=True)
    ceic_history = HistoricalRecords()

    def __str__(self):
        return self.ceic

class GrupoCargo(models.Model):
    class Meta:
        verbose_name = "Grupo Cargos"
        verbose_name_plural = "Grupos de Cargos"

    grupo_numero = models.DecimalField(max_digits=1, decimal_places=0, unique=True)
    grupocargo_history = HistoricalRecords()

class ActividadEspecifica(models.Model):
    class Meta:
        verbose_name = "Actividad Específica"
        verbose_name_plural = "Actividades Específicas"

    actividad_especifica_codigo = models.DecimalField(max_digits=2, decimal_places=0)
    actividad_especifica_nombre = models.CharField(max_length=100)
    actividad_especifica_history = HistoricalRecords()

    def __str__(self):
        return self.actividad_especifica_nombre

class Oficina(models.Model):
    class Meta:
        verbose_name = "Oficina"
        verbose_name_plural = "Oficinas"
    
    cargo_tipo = models.ForeignKey("CargoTipo", on_delete=models.CASCADE)
    cargo_directorio = models.ForeignKey("Directorio", on_delete=models.CASCADE, blank=True, null=True)
    cargo_gerencia = models.ForeignKey("Gerencia", on_delete=models.CASCADE, blank=True, null=True)
    cargo_direccion = models.ForeignKey("Direccion", on_delete=models.CASCADE, blank=True, null=True)
    cargo_departamento = models.ForeignKey("Departamento", on_delete=models.CASCADE, blank=True, null=True)
    cargos_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    cargos_history = HistoricalRecords()

    def __str__(self):
        gerencia = " - "+self.cargo_gerencia.gerencia_nombre if self.cargo_gerencia else ""
        direccion = " - "+self.cargo_direccion.direccion_nombre if self.cargo_direccion else ""
        departamento = " - "+self.cargo_departamento.departamento_nombre if self.cargo_departamento else ""
        return f"{self.cargo_tipo}{gerencia}{direccion}{departamento}"

class CargoTipo(models.Model):
    class Meta:
        # Ej. "Personal Transitorio, Contrato de Servicio, Planta Permanente, Gabinete, etc."
        verbose_name = "Tipo de Cargo"
        verbose_name_plural = "Tipos de Cargos"
    
    cargotipo = models.CharField("Tipo de Cargo", max_length=120)
    cargotipo_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    cargotipo_history = HistoricalRecords()

    def __str__(self):
        return self.cargotipo

class Directorio(models.Model):
    class Meta:
        # Ej. Presidencia, Vocalia 1, Vocalia 2, etc.
        verbose_name = "Directorio"
        verbose_name_plural = "Directorios"
    
    directorio_nombre = models.CharField("Directorio", max_length=200)
    directorio_autoridad_a_cargo = models.CharField("Autoridad a Cargo", max_length=200, null=True, blank=True)
    directorio_autoridad_a_cargo_fk = models.ForeignKey("Agente", on_delete=models.CASCADE, null=True, blank=True)
    directorio_cuof = models.CharField("CUOF", max_length=10)
    directorio_ungi = models.CharField("UNGI", max_length=10, null=True, blank=True)
    directorio_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    directorio_history = HistoricalRecords()

    def __str__(self):
        return self.directorio_nombre

class Gerencia(models.Model):
    class Meta:
        verbose_name = "Gerencia"
        verbose_name_plural = "Gerencias"

    gerencia_directorio = models.ForeignKey("Directorio", on_delete=models.CASCADE)
    gerencia_nombre = models.CharField("Gerencia", max_length=200)
    gerencia_autoridad_a_cargo = models.CharField("Autoridad a Cargo", max_length=200, null=True, blank=True)
    gerencia_autoridad_a_cargo_fk = models.ForeignKey("Agente", on_delete=models.CASCADE, null=True, blank=True)
    gerencia_cuof = models.CharField("CUOF", max_length=10)
    gerencia_ungi = models.CharField("UNGI", max_length=10, null=True, blank=True)
    gerencia_responsabilidadprimaria = models.TextField("Responsabilidad Primaria", null=True, blank=True)
    gerencia_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    gerencia_history = HistoricalRecords()

    def __str__(self):
        return self.gerencia_nombre

class Direccion(models.Model):
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"

    direccion_directorio = models.ForeignKey("Directorio", on_delete=models.CASCADE, null=True, blank=True)
    direccion_gerencia = models.ForeignKey("Gerencia", on_delete=models.CASCADE, null=True, blank=True)
    direccion_nombre = models.CharField("Direccion", max_length=200)
    direccion_autoridad_a_cargo = models.CharField("Autoridad a Cargo", max_length=200, null=True, blank=True)
    direccion_autoridad_a_cargo_fk = models.ForeignKey("Agente", on_delete=models.CASCADE, null=True, blank=True)
    direccion_cuof = models.CharField("CUOF", max_length=10)
    direccion_ungi = models.CharField("UNGI", max_length=10, null=True, blank=True)
    direccion_responsabilidadprimaria = models.TextField("Responsabilidad Primaria", null=True, blank=True)
    direccion_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    direccion_history = HistoricalRecords()

    def __str__(self):
        return self.direccion_nombre

class Departamento(models.Model):
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
    
    departamento_directorio = models.ForeignKey("Directorio", on_delete=models.CASCADE, null=True, blank=True)
    departamento_gerencia = models.ForeignKey("Gerencia", on_delete=models.CASCADE, null=True, blank=True)
    departamento_direccion = models.ForeignKey("Direccion", on_delete=models.CASCADE, null=True, blank=True)
    departamento_nombre = models.CharField("Departamento", max_length=200)
    departamento_autoridad_a_cargo = models.CharField("Autoridad a Cargo", max_length=200, null=True, blank=True)
    departamento_autoridad_a_cargo_fk = models.ForeignKey("Agente", on_delete=models.CASCADE, null=True, blank=True)
    departamento_cuof = models.CharField("CUOF", max_length=10)
    departamento_ungi = models.CharField("UNGI", max_length=10, null=True, blank=True)
    departamento_responsabilidadprimaria = models.TextField("Responsabilidad Primaria", null=True, blank=True)
    departamento_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    departamento_history = HistoricalRecords()

    def __str__(self):
        return self.departamento_nombre