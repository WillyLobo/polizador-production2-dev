import os
from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from core.validators import FileValidator, CuitValidator
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

    agente_usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
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
    cargo_interno = models.ForeignKey(
        "Oficina", verbose_name="Designación Temporal", related_name="agente_designacion_temporal",
        on_delete=models.CASCADE, blank=True, null=True,
        help_text="Oficina a la que el agente esta designado transitoriamente, distinta de su oficina habitual.",
    )
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
    tituloprofesional_abreviatura = models.CharField(max_length=10, null=True, blank=True)
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
        return f"{self.categoria_codigo} - {self.categoria_nombre}"

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

    def __str__(self):
        return str(self.grupo_numero)
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
    
    cargo_directorio = models.ForeignKey("Directorio", on_delete=models.CASCADE, blank=True, null=True)
    cargo_gerencia = models.ForeignKey("Gerencia", on_delete=models.CASCADE, blank=True, null=True)
    cargo_direccion = models.ForeignKey("Direccion", on_delete=models.CASCADE, blank=True, null=True)
    cargo_departamento = models.ForeignKey("Departamento", on_delete=models.CASCADE, blank=True, null=True)
    cargos_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    cargos_history = HistoricalRecords()

    def __str__(self):
        parts = [
            str(nivel) for nivel in
            (self.cargo_directorio, self.cargo_gerencia, self.cargo_direccion, self.cargo_departamento)
            if nivel
        ]
        return " - ".join(parts) if parts else f"Oficina {self.pk}"

    def clean(self):
        """Una Oficina es un nodo del arbol Directorio > Gerencia > Direccion > Departamento:
        se ubica en el nivel mas profundo que se le asigne (cargo_departamento, si no
        cargo_direccion, si no cargo_gerencia) y los niveles superiores se derivan de ese
        nodo en vez de elegirse por separado, para que no puedan quedar inconsistentes
        entre si (ej. una Direccion que en realidad depende de otra Gerencia)."""
        super().clean()

        if self.cargo_departamento_id:
            departamento = self.cargo_departamento
            direccion = departamento.departamento_direccion
            gerencia = departamento.departamento_gerencia or (direccion.direccion_gerencia if direccion else None)
            directorio = (
                departamento.departamento_directorio
                or (gerencia.gerencia_directorio if gerencia else None)
                or (direccion.direccion_directorio if direccion else None)
            )
        elif self.cargo_direccion_id:
            direccion = self.cargo_direccion
            gerencia = direccion.direccion_gerencia
            directorio = direccion.direccion_directorio or (gerencia.gerencia_directorio if gerencia else None)
        elif self.cargo_gerencia_id:
            direccion = None
            gerencia = self.cargo_gerencia
            directorio = gerencia.gerencia_directorio
        else:
            direccion = gerencia = directorio = None

        for field_name, expected in (
            ("cargo_direccion", direccion),
            ("cargo_gerencia", gerencia),
            ("cargo_directorio", directorio),
        ):
            if expected is None:
                continue
            current_id = getattr(self, f"{field_name}_id")
            if current_id and current_id != expected.id:
                raise ValidationError({
                    field_name: f"No coincide con la jerarquia del nivel mas especifico elegido (deberia ser '{expected}')."
                })
            setattr(self, field_name, expected)

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
    
class RepresentanteTecnico(models.Model):
    class Meta:
        verbose_name = "Representante Técnico"
        verbose_name_plural = "Representantes Técnicos"
        ordering = ("representantetecnico_apellido", "representantetecnico_nombre")
    
    representantetecnico_nombre = models.CharField("Nombre", max_length=200)
    representantetecnico_apellido = models.CharField("Apellido", max_length=200)
    representantetecnico_dni = models.DecimalField("DNI:", max_digits=9, decimal_places=0, unique=True, validators=[MinValueValidator(0)])
    representantetecnico_cuil = models.CharField("CUIT", max_length=13, validators=[CuitValidator()])
    representantetecnico_email = models.EmailField("Email", max_length=200, null=True, blank=True)
    representantetecnico_telefono = models.CharField("Telefono", max_length=200, null=True, blank=True)
    representantetecnico_profesion = models.ForeignKey("TituloProfesional", on_delete=models.CASCADE)
    representantetecnico_matricula = models.CharField("Matricula", max_length=10)
    representantetecnico_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    representantetecnico_history = HistoricalRecords()

    def __str__(self):
        return f"{self.representantetecnico_profesion.tituloprofesional_abreviatura} {self.representantetecnico_nombre} {self.representantetecnico_apellido}"

def generate_name_licenciapermiso(instance, filename):
    """Genera el nombre de archivo para el adjunto (certificado/comunicación) de una
    LicenciaPermiso."""
    directorio = "licencias/adjuntos/"
    extension = os.path.splitext(filename)[1]
    name = os.path.join(directorio, f"{instance.licenciapermiso_uuid}{extension}")
    return name

class TipoLicenciaPermiso(models.Model):
    class Meta:
        verbose_name = "Tipo de Licencia/Permiso"
        verbose_name_plural = "Tipos de Licencias/Permisos"
        ordering = ("tipolicenciapermiso_categoria", "tipolicenciapermiso_nombre")
        constraints = [
            models.UniqueConstraint(
                fields=["tipolicenciapermiso_categoria", "tipolicenciapermiso_nombre"],
                name="unique_tipolicenciapermiso_1"
            ),
        ]

    CATEGORIA = (
        ("LOR", "Licencia Ordinaria"),
        ("LEX", "Licencia Extraordinaria"),
        ("PER", "Permiso"),
    )
    UNIDAD = (
        ("DC", "Días corridos"),
        ("DH", "Días hábiles"),
        ("HS", "Horas"),
    )
    TOPE_PERIODO = (
        ("ANI", "Por año calendario"),
        ("VEZ", "Por vez/evento"),
        ("TOT", "Total del beneficio"),
        ("VAR", "Variable"),
    )
    REMUNERADA = (
        ("SI", "Con goce de haberes"),
        ("NO", "Sin goce de haberes"),
        ("PA", "Parcial"),
    )

    tipolicenciapermiso_categoria = models.CharField("Categoría", max_length=3, choices=CATEGORIA)
    tipolicenciapermiso_nombre = models.CharField("Nombre", max_length=150)
    tipolicenciapermiso_articulo = models.CharField("Artículo (Ley 645-A)", max_length=20, blank=True, null=True)
    tipolicenciapermiso_unidad = models.CharField("Unidad", max_length=2, choices=UNIDAD, default="DC")
    tipolicenciapermiso_tope_cantidad = models.PositiveIntegerField("Tope", blank=True, null=True, help_text="Vacío cuando el tope no es un número fijo (ej. depende de la antigüedad o de junta médica).")
    tipolicenciapermiso_tope_periodo = models.CharField("Período del tope", max_length=3, choices=TOPE_PERIODO, default="ANI")
    tipolicenciapermiso_remunerada = models.CharField("Remunerada", max_length=2, choices=REMUNERADA, default="SI")
    tipolicenciapermiso_antiguedad_meses = models.PositiveIntegerField("Antigüedad mínima (meses)", default=0)
    tipolicenciapermiso_requiere_certificado = models.BooleanField("Requiere certificado", default=False)
    tipolicenciapermiso_compensacion_horaria = models.BooleanField("Requiere compensación de horario", default=False, help_text="Permisos que la ley obliga a devolver con horas de trabajo (ej. razones particulares, lactancia).")
    tipolicenciapermiso_observaciones = models.TextField("Observaciones", blank=True, null=True)
    tipolicenciapermiso_activo = models.BooleanField("Activo", default=True)
    tipolicenciapermiso_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    tipolicenciapermiso_history = HistoricalRecords()

    def __str__(self):
        return f"{self.tipolicenciapermiso_nombre} ({self.get_tipolicenciapermiso_categoria_display()})"

class LicenciaPermiso(models.Model):
    """Registro administrativo de una licencia/permiso ya otorgado a un agente (no hay
    flujo de solicitud/aprobación: se carga el hecho consumado, respaldado o no por un
    instrumento legal formal)."""
    class Meta:
        verbose_name = "Licencia/Permiso"
        verbose_name_plural = "Licencias/Permisos"
        ordering = ("-licenciapermiso_fecha_desde",)

    licenciapermiso_agente = models.ForeignKey("Agente", verbose_name="Agente", on_delete=models.CASCADE)
    licenciapermiso_tipo = models.ForeignKey("TipoLicenciaPermiso", verbose_name="Tipo", on_delete=models.CASCADE)
    licenciapermiso_fecha_otorgamiento = models.DateField("Fecha de Otorgamiento", default=timezone.now)
    licenciapermiso_fecha_desde = models.DateField("Fecha Desde")
    licenciapermiso_fecha_hasta = models.DateField("Fecha Hasta", blank=True, null=True)
    licenciapermiso_cantidad = models.PositiveIntegerField("Cantidad", help_text="En la unidad indicada por el tipo (días u horas).")
    licenciapermiso_motivo = models.TextField("Motivo", blank=True, null=True)
    licenciapermiso_anulada = models.BooleanField("Anulada", default=False, help_text="Si el registro se encuentra anulado, no se computa en los balances ni reportes.")
    licenciapermiso_instrumento_resolucion = models.ForeignKey("secretariador.InstrumentosLegalesResoluciones", verbose_name="Resolución", on_delete=models.CASCADE, blank=True, null=True)
    licenciapermiso_instrumento_decreto = models.ForeignKey("secretariador.InstrumentosLegalesDecretos", verbose_name="Decreto", on_delete=models.CASCADE, blank=True, null=True)
    licenciapermiso_instrumento_memorandum = models.ForeignKey("secretariador.InstrumentosLegalesMemorandum", verbose_name="Memorandum", on_delete=models.CASCADE, blank=True, null=True)
    licenciapermiso_adjunto = models.FileField(
        "Adjunto (certificado/comunicación)", upload_to=generate_name_licenciapermiso, max_length=500,
        validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf",))],
        blank=True, null=True,
    )
    licenciapermiso_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    licenciapermiso_history = HistoricalRecords()

    def clean(self):
        super().clean()
        instrumentos = [
            self.licenciapermiso_instrumento_resolucion_id,
            self.licenciapermiso_instrumento_decreto_id,
            self.licenciapermiso_instrumento_memorandum_id,
        ]
        if sum(1 for i in instrumentos if i) > 1:
            raise ValidationError("Solo se puede vincular un instrumento legal (Resolución, Decreto o Memorandum).")
        if self.licenciapermiso_fecha_hasta and self.licenciapermiso_fecha_hasta < self.licenciapermiso_fecha_desde:
            raise ValidationError({"licenciapermiso_fecha_hasta": "No puede ser anterior a la fecha desde."})

    def __str__(self):
        return f"{self.licenciapermiso_tipo} - {self.licenciapermiso_agente} ({self.licenciapermiso_fecha_desde})"

class DevolucionHorasPermiso(models.Model):
    class Meta:
        verbose_name = "Devolución de Horas"
        verbose_name_plural = "Devoluciones de Horas"
        ordering = ("devolucionhoras_fecha",)

    devolucionhoras_licencia = models.ForeignKey("LicenciaPermiso", verbose_name="Licencia/Permiso", on_delete=models.CASCADE, related_name="devolucionhoras_set")
    devolucionhoras_fecha = models.DateField("Fecha")
    devolucionhoras_cantidad = models.PositiveIntegerField("Horas Devueltas")
    devolucionhoras_observaciones = models.CharField("Observaciones", max_length=300, blank=True, null=True)
    devolucionhoras_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    devolucionhoras_history = HistoricalRecords()

    def __str__(self):
        return f"{self.devolucionhoras_cantidad}hs - {self.devolucionhoras_fecha}"