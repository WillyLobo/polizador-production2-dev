from docxtpl import DocxTemplate

"""
Ideas:
    - El formulario debería cargarse con un solicitante y X cantidad de comisionados.
    - El solicitante puede ser parte de los comisionados.

Campos:
    - Modelo Agente:
        - particula // sexo = el/la // Masculino/Femenino
        - abreviatura = Sr./Sra./Dr./Dra./Etc
        - cargo = "Vocal"
        - nombre = "Diego Fernando GUTIERREZ"
        - dni = 27207092
        - cuil = "20-27207092-0"
    - Modelo Solicitud:
        - actuacion = "E-10-2024-3081-AE"
        - Solicitantes_involucrados = []
        - localidades = ["Juan José Castelli", "Quitilipi"]
        - fecha = str("14/03/2024")
        - tareas = "visitas a planes de viviendas entregados y atención de demanda de vecinos y operativos en dicha localidad"
        - vehiculo = "Toyota Hilux – Chapa Patente AE 939 TX"
        - dia_inhabil = bool(False)
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

class Solicitante:
    particula = "el"
    abreviatura = "Dr."
    cargo = "Vocal"
    nombre = "Diego Fernando GUTIERREZ"
    dni = 27207092
    cuil = "20-27207092-0"

agentes = [
    ["la", "Dra.", "", "Natalia PERINO CINTAS", "27410089", "27-27410089-9"],
    ["el", "Sr.", "", "Emanuel GONZALEZ", "31698732", "20-31698732-0"]
    ]
localidades = ["Juan José Castelli", "Quitilipi"]

doc = DocxTemplate("template.docx")
context = { 
    "agente_cargo" : Solicitante.cargo,
    "agente_abreviatura" : Solicitante.abreviatura,
    "agente_nombre" : Solicitante.nombre,
    "comisionados" : agentes,
    "localidades" : localidades
    }
doc.render(context)
doc.save("demo.docx")