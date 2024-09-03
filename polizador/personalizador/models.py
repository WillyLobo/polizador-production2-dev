from django.db import models
from django.core.validators import MinValueValidator
from secretariador.functions import FileValidator, CuitValidator


# class Agente(models.Model):
#     SEXO = (
#         ("M", "Masculino"),
#         ("F", "Femenino")
#     )
#     TITULO = (
#         ("S", "Secundario"),
#         ("T", "Terciario"),
#         ("U", "Universitario")
#     )
#     CATEGORIA = (
#         ("P5", "Profesional 5"),
#         ("A5", "Administrativo 5"),
#         ("A6", "Administrativo 6")
#     )
#     agente_secretariador = models.OneToOneField("secretariador.Comisionado", on_delete=models.CASCADE, primary_key=True)
#     n_legajo = models.IntegerField(primary_key=True)
#     sexo = models.CharField(max_length=1, choices=SEXO)
#     apellidos = models.CharField(max_length=200)
#     nombres = models.CharField(max_length=200)
#     dni = models.DecimalField("DNI:", max_digits=9, decimal_places=0, validators=[MinValueValidator(0)])
#     cuil = models.CharField("CUIT", max_length=13, validators=[CuitValidator()])
#     fecha_nacimiento = models.DateField()
#     # edad = generatedfield(current_date - fecha_nacimiento)
#     fecha_ingreso = models.DateField()
#     n_resolucion_de_contrato = models.CharField(max_length=13)
#     fecha_pase_a_planta = models.DateField() # fecha utilizada para el computo de antiguedad.
#     n_decreto = models.CharField(max_length=10)
#     titulo_profesional = models.CharField(max_length=1, choices=TITULO)
#     titulo_tipo = models.CharField(max_length=500)
#     n_resolucion_bonificacion = models.CharField(max_length=13)
#     porcentaje_bonificacion = models.DecimalField(max_digits=5, decimal_places=2)
#     # Ver reglamentaciones, quiza corresponda crear tablas de los siguientes campos:
#     categoria = models.ForeignKey("Categoria", on_delete=models.CASCADE)
#     apartado = models.CharField(max_length=1)
#     ceic = models.IntegerField( validators=[MinValueValidator(0)])
#     grupo = models.IntegerField(validators=[MinValueValidator(0)])
#     activdad_central = models.IntegerField()
#     actividad_especifica = models.CharField(max_length=500)
#     cuof_gerencia = models.IntegerField(validators=[MinValueValidator(0)])
#     gerencia = models.CharField(max_length=300)
#     cuof_departamento_o_direccion = models.IntegerField(validators=[MinValueValidator(0)])
#     n_decreto_transferencia_definitiva = models.CharField(max_length=10)
#     cargo_interno = models.CharField(max_length=300)
#     n_resolucion_cargo_interno = models.CharField(max_length=13)
#     domicilio_direccion = models.CharField(max_length=500)
#     domicilio_barrio = models.CharField(max_length=300)
#     domicilio_localidad = models.ForeignKey("carga.Localidad", on_delete=models.CASCADE)
#     # Campos calculados en base a lo que diga la fecha de la resolucion de aportes.
#     # Extraer años, meses, dias para computar.
#     aportes_ley_resolucion = models.CharField(max_length=13)
#     # aportes_ley = generatedfield(delta de fecha_desde a fecha_hasta)
#     # aportes_anses = generatedfield(delta de anses_fecha_desde a anses_fecha_hasta)
#     # años_totales = generatedfield(delta de fecha_de_igreso a hoy)
#     fecha_carga_interna = models.DateField()

#     class Categoria(models.Model):
#         pass

class Cargos(models.Model):
    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
    
    cargo_tipo = models.ForeignKey("CargoTipo", on_delete=models.CASCADE)
    cargo_gerencia = models.ForeignKey("Gerencia", on_delete=models.CASCADE, blank=True, null=True)
    cargo_direccion = models.ForeignKey("Direccion", on_delete=models.CASCADE, blank=True, null=True)
    cargo_departamento = models.ForeignKey("Departamento", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        gerencia = " - "+self.cargo_gerencia.gerencia_nombre if self.cargo_gerencia else ""
        direccion = " - "+self.cargo_direccion.direccion_nombre if self.cargo_direccion else ""
        departamento = " - "+self.cargo_departamento.departamento_nombre if self.cargo_departamento else ""
        return f"{self.cargo_tipo}{gerencia}{direccion}{departamento}"

class CargoTipo(models.Model):
    class Meta:
        verbose_name = "Tipo de Cargo"
        verbose_name_plural = "Tipos de Cargos"
    
    cargotipo = models.CharField("Tipo de Cargo", max_length=120)

    def __str__(self):
        return self.cargotipo

class Gerencia(models.Model):
    class Meta:
        verbose_name = "Gerencia"
        verbose_name_plural = "Gerencias"
    
    gerencia_nombre = models.CharField("Gerencia", max_length=200)
    gerencia_cuof = models.CharField("CUOF", max_length=10)

    def __str__(self):
        return self.gerencia_nombre

class Direccion(models.Model):
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"

    direccion_nombre = models.CharField("Direccion", max_length=200)
    direccion_cuof = models.CharField("CUOF", max_length=10)

    def __str__(self):
        return self.direccion_nombre

class Departamento(models.Model):
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
    
    departamento_nombre = models.CharField("Departamento", max_length=200)
    departamento_cuof = models.CharField("CUOF", max_length=10)

    def __str__(self):
        return self.departamento_nombre

