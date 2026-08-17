import os
from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from core.validators import FileValidator, CuitValidator
from dateutil.relativedelta import relativedelta
from uuid_utils import compat

class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"

def abreviatura_default_por_sexo(sexo):
    """Sr./Sra. según GeneroAgente, usado como default cuando no se carga
    una abreviatura explícita (mismo criterio Masculino/Femenino que ya se
    usa en el resto del código para "el"/"la")."""
    return "Sr." if sexo.generoagente_nombre == "Masculino" else "Sra."

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
    abreviatura = models.CharField("Abreviatura", max_length=10, blank=True, null=True, help_text="Sr./Sra.")
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
    n_decreto = models.CharField(max_length=10, blank=True, null=True, help_text="N° de instrumento de pase a planta permanente - Solo Numero/Año")
    INSTRUMENTO_BONIFICACION_TIPO = (
        ("RES", "Resolución"),
        ("DEC", "Decreto"),
    )
    instrumento_bonificacion_tipo = models.CharField("Tipo de instrumento", max_length=3, choices=INSTRUMENTO_BONIFICACION_TIPO, blank=True, null=True)
    instrumento_bonificacion = models.CharField(max_length=13, blank=True, null=True, help_text="Instrumento que aprueba la bonificacion por titulo - Solo Numero/Año")
    porcentaje_bonificacion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    INSTRUMENTO_CONTRATO_DE_SERVICIO_TIPO = (
        ("RES", "Resolución"),
        ("DEC", "Decreto"),
    )
    instrumento_contrato_de_servicio_tipo = models.CharField("Tipo de instrumento", max_length=3, choices=INSTRUMENTO_CONTRATO_DE_SERVICIO_TIPO, blank=True, null=True)
    instrumento_contrato_de_servicio = models.CharField(max_length=13, blank=True, null=True, help_text="Instrumento que aprueba el contrato de servicio - Solo Numero/Año")
    categoria = models.ForeignKey("Categoria", on_delete=models.CASCADE, blank=True, null=True)
    denominacion_cargo = models.ForeignKey("DenominacionCargo", related_name="agente_denominacion_cargo", on_delete=models.CASCADE, blank=True, null=True)
    cargo_interno = models.ForeignKey(
        "Oficina", verbose_name="Designación Temporal", related_name="agente_designacion_temporal",
        on_delete=models.CASCADE, blank=True, null=True,
        help_text="Oficina a la que el agente esta designado transitoriamente, distinta de su oficina habitual.",
    )
    INSTRUMENTO_CARGO_INTERNO_TIPO = (
        ("RES", "Resolución"),
        ("DEC", "Decreto"),
    )
    instrumento_cargo_interno_tipo = models.CharField("Tipo de instrumento", max_length=3, choices=INSTRUMENTO_CARGO_INTERNO_TIPO, blank=True, null=True)
    instrumento_cargo_interno = models.CharField("Instrumento de designación temporal", max_length=13, blank=True, null=True, help_text="Número de instrumento de designación temporal - Solo Numero/Año")
    apartado = models.ForeignKey("ApartadoCargo", on_delete=models.CASCADE, blank=True, null=True)
    ceic = models.ForeignKey("CEIC", on_delete=models.CASCADE, blank=True, null=True)
    grupo = models.ForeignKey("GrupoCargo", on_delete=models.CASCADE, blank=True, null=True)
    activdad_central = models.CharField(max_length=1, default="1")
    actividad_especifica = models.ForeignKey("ActividadEspecifica", on_delete=models.CASCADE, blank=True, null=True)
    oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE, blank=True, null=True)
    n_decreto_transferencia_definitiva = models.CharField(max_length=10, blank=True, null=True, help_text="Decreto de transferencia definitiva - Solo Numero/Año")
    domicilio_direccion = models.CharField("Dirección", max_length=500, blank=True, null=True)
    domicilio_barrio = models.CharField("Barrio", max_length=300, blank=True, null=True)
    domicilio_localidad = models.ForeignKey("carga.Localidad", on_delete=models.CASCADE, blank=True, null=True)
    domicilio_provincia = models.ForeignKey("carga.Provincia", on_delete=models.CASCADE, blank=True, null=True)
    # Antigüedad reconocida por instrumentos legales, adicional a la que surge de fecha_ingreso.
    APORTES_LEY_RESOLUCION_TIPO = (
        ("DEC", "Decreto"),
        ("RES", "Resolución"),
        ("DIS", "Disposición"),
    )
    aportes_ley_resolucion_tipo = models.CharField("Tipo de instrumento", max_length=3, choices=APORTES_LEY_RESOLUCION_TIPO, blank=True, null=True)
    aportes_ley_resolucion = models.CharField(max_length=13, blank=True, null=True, help_text="Instrumento que establece los aportes - Solo Numero/Año")
    aportes_ley_resolucion_anios = models.PositiveIntegerField("Años reconocidos (Resolución)", default=0, blank=True)
    aportes_ley_resolucion_meses = models.PositiveIntegerField("Meses reconocidos (Resolución)", default=0, blank=True)
    aportes_ley_resolucion_dias = models.PositiveIntegerField("Días reconocidos (Resolución)", default=0, blank=True)
    aportes_anses = models.CharField(max_length=13, blank=True, null=True, help_text="Instrumento que establece los aportes")
    aportes_anses_anios = models.PositiveIntegerField("Años reconocidos (ANSES)", default=0, blank=True)
    aportes_anses_meses = models.PositiveIntegerField("Meses reconocidos (ANSES)", default=0, blank=True)
    aportes_anses_dias = models.PositiveIntegerField("Días reconocidos (ANSES)", default=0, blank=True)
    # FLAGS
    activo = models.BooleanField("Activo", default=True)
    con_errores = models.BooleanField(
        "Con errores de carga", default=False,
        help_text="Se marca automaticamente al importar personal_gral.xlsx si la fila tuvo algun aviso.",
    )
    agente_verificado_contra_padron = models.BooleanField("Chequeado",default=False, help_text="Los datos fueron verificados contra el padrón electoral")
    agente_es_inpector_obra = models.BooleanField("Inspector de Obra",default=False, help_text="El agente es inspector de obra")
    agente_personal_transitorio = models.BooleanField("Personal Transitorio",default=False, help_text="Tildar si el agente es personal transitorio")
    agente_personal_de_gabinete = models.BooleanField("Personal de Gabinete",default=False, help_text="Tildar si el agente es personal de gabinete")
    # Otros
    agente_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    agente_history = HistoricalRecords()

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None
        return relativedelta(timezone.localdate(), self.fecha_nacimiento).years

    @property
    def antiguedad(self):
        """Antigüedad total: años/meses/días desde fecha_ingreso hasta hoy, más los
        reconocidos por aportes_ley_resolucion y aportes_anses. Convención de cómputo
        de aportes: 30 días = 1 mes, 12 meses = 1 año."""
        if not self.fecha_ingreso:
            return None

        delta = relativedelta(timezone.localdate(), self.fecha_ingreso)
        anios = delta.years + self.aportes_ley_resolucion_anios + self.aportes_anses_anios
        meses = delta.months + self.aportes_ley_resolucion_meses + self.aportes_anses_meses
        dias = delta.days + self.aportes_ley_resolucion_dias + self.aportes_anses_dias

        meses += dias // 30
        dias %= 30
        anios += meses // 12
        meses %= 12

        return {"anios": anios, "meses": meses, "dias": dias}

    def __str__(self):
        if self.agente_personal_transitorio:
            return f"(C){self.agente_nombreyapellido} - DNI Nº{self.dni}"
        else:
            return f"{self.agente_nombreyapellido} - DNI Nº{self.dni}"

    def save(self, *args, **kwargs):
        if not self.abreviatura:
            self.abreviatura = abreviatura_default_por_sexo(self.sexo)
        super().save(*args, **kwargs)

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
   
    tituloprofesional_nombre = models.CharField(max_length=200, help_text="Nombre del título profesional sin abreviaturas. Ej. Técnico Superior en Administración, NO Tec. Sup. en Adm.")
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

class ComisionadoExterno(models.Model):
    """Persona externa al Instituto (de otro organismo, contratada puntualmente,
    etc.) que puede ser comisionada a viajar en una Solicitud de viáticos, sin
    ser un empleado (personalizador.Agente) — no debe aparecer en reportes de
    RRHH/organigrama/nómina. Expone los mismos nombres de atributo que Agente
    para el subconjunto de datos que necesita el circuito de viáticos
    (secretariador.ComisionadoSolicitud.persona)."""
    class Meta:
        verbose_name = "Comisionado Externo"
        verbose_name_plural = "Comisionados Externos"
        ordering = ("agente_apellidos", "agente_nombres")

    agente_nombres = models.CharField("Nombres", max_length=120)
    agente_apellidos = models.CharField("Apellidos", max_length=120)
    agente_nombreyapellido = models.GeneratedField(
        expression=ConcatOp(models.F("agente_nombres"), models.Value(" "), models.F("agente_apellidos")),
        output_field=models.CharField("Nombre y Apellido", max_length=256, editable=False),
        db_persist=True
    )
    abreviatura = models.CharField("Abreviatura", max_length=10, blank=True, null=True, help_text="Sr./Sra.")
    sexo = models.ForeignKey("GeneroAgente", on_delete=models.CASCADE)
    dni = models.DecimalField("DNI:", max_digits=9, decimal_places=0, unique=True, validators=[MinValueValidator(0)])
    cuil = models.CharField("CUIT", max_length=13, validators=[CuitValidator()])
    institucion_origen = models.CharField("Institución de origen", max_length=200, blank=True, null=True, help_text="Organismo/empresa al que pertenece.")
    comisionadoexterno_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    comisionadoexterno_history = HistoricalRecords()

    def __str__(self):
        return f"(Externo) {self.agente_nombreyapellido} - DNI Nº{self.dni}"

    def save(self, *args, **kwargs):
        if not self.abreviatura:
            self.abreviatura = abreviatura_default_por_sexo(self.sexo)
        super().save(*args, **kwargs)

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
        return f"{self.tipolicenciapermiso_articulo} - {self.tipolicenciapermiso_nombre} ({self.get_tipolicenciapermiso_categoria_display()})"

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
    licenciapermiso_saldo_de_corte = models.ForeignKey(
        "CorteLicencia", verbose_name="Usa saldo de corte", related_name="usos_saldo",
        on_delete=models.PROTECT, blank=True, null=True,
        help_text="Completar si esta licencia consume el saldo pendiente de un corte anterior, en vez de ser un otorgamiento nuevo.",
    )
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

        if self.licenciapermiso_saldo_de_corte_id:
            corte = self.licenciapermiso_saldo_de_corte
            licencia_original = corte.cortelicencia_licencia
            if self.licenciapermiso_agente_id and self.licenciapermiso_agente_id != licencia_original.licenciapermiso_agente_id:
                raise ValidationError({"licenciapermiso_saldo_de_corte": "El corte pertenece a otro agente."})
            if self.licenciapermiso_tipo_id and self.licenciapermiso_tipo_id != licencia_original.licenciapermiso_tipo_id:
                raise ValidationError({"licenciapermiso_saldo_de_corte": "El corte corresponde a otro tipo de licencia."})
            if self.licenciapermiso_fecha_desde and self.licenciapermiso_fecha_desde > corte.cortelicencia_fecha_vencimiento:
                raise ValidationError({"licenciapermiso_fecha_desde": f"El saldo del corte vence el {corte.cortelicencia_fecha_vencimiento}."})
            if self.licenciapermiso_cantidad is not None and not self.licenciapermiso_anulada:
                restante = corte.dias_restantes
                if self.pk:
                    anterior = LicenciaPermiso.objects.filter(pk=self.pk).values_list(
                        "licenciapermiso_cantidad", "licenciapermiso_anulada").first()
                    if anterior and not anterior[1]:
                        restante += anterior[0]
                if self.licenciapermiso_cantidad > restante:
                    raise ValidationError({"licenciapermiso_cantidad": f"Supera el saldo pendiente del corte ({restante})."})

        if (self.licenciapermiso_tipo_id and self.licenciapermiso_agente_id and self.licenciapermiso_fecha_desde
                and self.licenciapermiso_cantidad is not None and not self.licenciapermiso_anulada):
            from personalizador.licencias import LICENCIA_ANUAL_ADELANTADA_NOMBRE, balance_tipo

            tipo = self.licenciapermiso_tipo
            if tipo.tipolicenciapermiso_categoria == "LOR" and tipo.tipolicenciapermiso_nombre == LICENCIA_ANUAL_ADELANTADA_NOMBRE:
                anio = self.licenciapermiso_fecha_desde.year
                disponible = balance_tipo(self.licenciapermiso_agente, tipo, anio)["disponibles"]
                if disponible is not None:
                    if self.pk:
                        anterior = LicenciaPermiso.objects.filter(pk=self.pk).values_list(
                            "licenciapermiso_cantidad", "licenciapermiso_anulada").first()
                        if anterior and not anterior[1]:
                            disponible += anterior[0]
                    if self.licenciapermiso_cantidad > disponible:
                        raise ValidationError({"licenciapermiso_cantidad": f"Supera el cupo disponible del año siguiente para adelantar ({disponible})."})

    def __str__(self):
        return f"{self.licenciapermiso_tipo} - {self.licenciapermiso_agente} ({self.licenciapermiso_fecha_desde})"

def generate_name_cortelicencia(instance, filename):
    """Genera el nombre de archivo para el adjunto (nota) de un CorteLicencia."""
    directorio = "licencias/cortes/"
    extension = os.path.splitext(filename)[1]
    name = os.path.join(directorio, f"{instance.cortelicencia_uuid}{extension}")
    return name

class CorteLicencia(models.Model):
    """Interrupción de una Licencia Anual (Ordinaria o de Invierno) ya otorgada:
    el agente se reintegra a sus tareas por necesidades del organismo antes de agotar
    los días, y el saldo pendiente queda disponible para usarse después (total o
    fraccionado, ver `LicenciaPermiso.licenciapermiso_saldo_de_corte`) hasta la fecha
    de vencimiento."""
    class Meta:
        verbose_name = "Corte de Licencia"
        verbose_name_plural = "Cortes de Licencia"

    cortelicencia_licencia = models.OneToOneField(
        "LicenciaPermiso", verbose_name="Licencia interrumpida",
        on_delete=models.CASCADE, related_name="corte",
    )
    cortelicencia_fecha_reintegro = models.DateField("Fecha de Reintegro")
    cortelicencia_dias_gozados = models.PositiveIntegerField("Días Gozados", help_text="Días efectivamente usados antes del reintegro.")
    cortelicencia_dias_pendientes = models.PositiveIntegerField("Días Pendientes", help_text="Saldo a utilizar más adelante (total o fraccionado).")
    cortelicencia_fecha_vencimiento = models.DateField("Vence el", help_text="Fecha límite para usar el saldo pendiente.")
    cortelicencia_motivo = models.TextField("Motivo", blank=True, null=True, help_text='Ej. "Necesidades del organismo".')
    # Nota/actuación administrativa (no es un instrumento legal formal): mismo patrón
    # de campos que secretariador.Solicitud.solicitud_actuacion.
    cortelicencia_nota_jurisdiccion = models.CharField("Jurisdicción", max_length=3, default="E10")
    cortelicencia_nota_numero = models.DecimalField("N° Actuación", max_digits=6, decimal_places=0, validators=[MinValueValidator(0)], default=0)
    cortelicencia_nota_ano = models.DecimalField("Año Actuación", max_digits=4, decimal_places=0, validators=[MinValueValidator(0)], default=int(timezone.now().year))
    cortelicencia_nota_actuacion = models.GeneratedField(
        expression=ConcatOp('cortelicencia_nota_jurisdiccion', models.Value("-"), 'cortelicencia_nota_numero', models.Value("-"), 'cortelicencia_nota_ano'),
        output_field=models.CharField("N° Actuación", max_length=20, editable=False),
        db_persist=True,
    )
    cortelicencia_adjunto = models.FileField(
        "Adjunto (nota)", upload_to=generate_name_cortelicencia, max_length=500,
        validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf",))],
        blank=True, null=True,
    )
    cortelicencia_uuid = models.UUIDField(default=compat.uuid7, editable=False)
    cortelicencia_history = HistoricalRecords()

    def clean(self):
        super().clean()
        from personalizador.licencias import LICENCIA_ANUAL_ORDINARIA_NOMBRE, LICENCIA_ANUAL_INVIERNO_NOMBRE

        licencia = self.cortelicencia_licencia
        if self.cortelicencia_licencia_id:
            if licencia.licenciapermiso_tipo.tipolicenciapermiso_nombre not in (
                LICENCIA_ANUAL_ORDINARIA_NOMBRE, LICENCIA_ANUAL_INVIERNO_NOMBRE,
            ):
                raise ValidationError({"cortelicencia_licencia": "Solo se puede registrar un corte sobre una Licencia Anual (Ordinaria o de Invierno)."})

            if self.cortelicencia_fecha_reintegro:
                if self.cortelicencia_fecha_reintegro < licencia.licenciapermiso_fecha_desde:
                    raise ValidationError({"cortelicencia_fecha_reintegro": "No puede ser anterior a la fecha desde de la licencia."})
                if licencia.licenciapermiso_fecha_hasta and self.cortelicencia_fecha_reintegro > licencia.licenciapermiso_fecha_hasta:
                    raise ValidationError({"cortelicencia_fecha_reintegro": "No puede ser posterior a la fecha hasta de la licencia."})

            if self.cortelicencia_dias_gozados is not None and self.cortelicencia_dias_pendientes is not None:
                if self.cortelicencia_dias_gozados + self.cortelicencia_dias_pendientes > licencia.licenciapermiso_cantidad:
                    raise ValidationError("Días gozados + días pendientes no puede superar la cantidad total de la licencia.")

        if (self.cortelicencia_fecha_reintegro and self.cortelicencia_fecha_vencimiento
                and self.cortelicencia_fecha_vencimiento <= self.cortelicencia_fecha_reintegro):
            raise ValidationError({"cortelicencia_fecha_vencimiento": "Debe ser posterior a la fecha de reintegro."})

    @property
    def dias_usados_saldo(self):
        return self.usos_saldo.filter(licenciapermiso_anulada=False).aggregate(
            total=models.Sum("licenciapermiso_cantidad"))["total"] or 0

    @property
    def dias_restantes(self):
        return self.cortelicencia_dias_pendientes - self.dias_usados_saldo

    @property
    def vencido(self):
        return self.dias_restantes > 0 and self.cortelicencia_fecha_vencimiento < timezone.localdate()

    def __str__(self):
        return f"Corte - {self.cortelicencia_licencia} ({self.cortelicencia_fecha_reintegro})"

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