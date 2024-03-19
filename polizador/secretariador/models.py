from django.db import models
from django.core.validators import MinValueValidator
from secretariador.functions import validar_cuit

"""
Ideas:
    - El formulario debería cargarse con un solicitante y X cantidad de comisionados.
    - El solicitante puede ser parte de los comisionados.

Campos:
    - Modelo Agente:
        x particula // sexo = el/la // Masculino/Femenino
        x abreviatura = Sr./Sra./Dr./Dra./Etc
        x cargo = FK -> Organigrama
        x nombre = "Diego Fernando GUTIERREZ"
        x dni = 27207092
        x cuil = "20-27207092-0"
    - Modelo Organigrama:
        x Cargo: "Vocal/Director de Obras de Vivienda/Jefe Departamento Auditoria/Etc"
    - Modelo Solicitud:
        x actuacion = "E-10-2024-3081-AE"
        x Solicitantes_involucrados = []
        x localidades = ["Juan José Castelli", "Quitilipi"]
        x fecha
            desde = str("14/03/2024")
            hasta = str("14/03/2024")
        x tareas = "visitas a planes de viviendas entregados y atención de demanda de vecinos y operativos en dicha localidad"
        x vehiculo = FK -> Vehiculo
        x dia_inhabil = bool(False)
        - combustible
        - gastos
    - Modelo Vehiculo:
        x Modelo: "Toyota Hilux"
        x Patente: "Chapa Patente AE 939 TX"
    /----------------Formularios--------------------/    
    - Formulario Solicitud:
        - actuacion = "E-10-2024-3081-AE"
        - Solicitantes_involucrados:
            - Agente = Abreviatura + Nombre
            - Caracter de colaborador = bool()
            - Chofer = bool()
        - localidades = ["Juan José Castelli", "Quitilipi"]
        - fecha = str("14/03/2024")
        - tareas = "visitas a planes de viviendas entregados y atención de demanda de vecinos y operativos en dicha localidad"
        - vehiculo = "Toyota Hilux – Chapa Patente AE 939 TX"
        - dia_inhabil = bool(False)
        
"""

class Comisionado(models.Model):
    class Meta:
        verbose_name = "Comisionado"
        verbose_name_plural = "Comisionados"
    SEXO = (
        ("M", "Masculino"),
        ("F", "Femenino")
    )
    comisionado_nombre = models.CharField("Nombre", max_length=120)
    comisionado_abreviatura = models.CharField("Abreviatura", max_length=10)
    comisionado_sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    comisionado_cargo = models.ForeignKey("Organigrama", on_delete=models.CASCADE)
    comisionado_dni = models.DecimalField("DNI:", max_digits=9, decimal_places=0, validators=[MinValueValidator(0)])
    comisionado_cuit = models.CharField("CUIT", max_length=13, validators=[validar_cuit])

class Organigrama(models.Model):
    organigrama_cargo = models.CharField("Cargo", max_length=120)

class Vehiculo(models.Model):
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    vehiculo_modelo = models.CharField("Modelo", max_length=100)
    vehiculo_patente = models.CharField("Patente", max_length=9)


class Solicitud(models.Model):
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

    solicitud_actuacion = models.CharField("Actuación", max_length=18)
    solicitud_involucrados = models.ManyToManyField("Comisionado", related_name="solicitud_comisionados", verbose_name="Involucrados")
    # Cada involucrado tiene Viaticos // Campo booleano indicando el chofer // Si es chofer... incluye el combustible // gastos extra
    solicitud_localidades = models.ManyToManyField("carga.Localidad")
    solicitud_fecha_desde = models.DateField("Fecha Inicio")
    solicitud_fecha_hasta = models.DateField("Fecha Regreso")
    solicitud_tareas = models.TextField("Tareas a Realizar")
    solicitud_vehiculo = models.ForeignKey("Vehiculo", on_delete=models.CASCADE)
    solicitud_dia_inhabil = models.BooleanField("Dia Inhábil")



