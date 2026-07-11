from django.core.management.base import BaseCommand, CommandError
from personalizador.models import Agente
import sqlite3
import time

# class Style:
#     def ERROR(self, text: str) -> str: ...
#     def SUCCESS(self, text: str) -> str: ...
#     def WARNING(self, text: str) -> str: ...
#     def NOTICE(self, text: str) -> str: ...
#     def SQL_FIELD(self, text: str) -> str: ...
#     def SQL_COLTYPE(self, text: str) -> str: ...
#     def SQL_KEYWORD(self, text: str) -> str: ...
#     def SQL_TABLE(self, text: str) -> str: ...
#     def HTTP_INFO(self, text: str) -> str: ...
#     def HTTP_SUCCESS(self, text: str) -> str: ...
#     def HTTP_REDIRECT(self, text: str) -> str: ...
#     def HTTP_NOT_MODIFIED(self, text: str) -> str: ...
#     def HTTP_BAD_REQUEST(self, text: str) -> str: ...
#     def HTTP_NOT_FOUND(self, text: str) -> str: ...
#     def HTTP_SERVER_ERROR(self, text: str) -> str: ...
#     def MIGRATE_HEADING(self, text: str) -> str: ...
#     def MIGRATE_LABEL(self, text: str) -> str: ...
#     def ERROR_OUTPUT(self, text: str) -> str: ...

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="No guarda cambios en la base de datos, solo muestra lo que haría.",
        )

    def handle(self, *args, **kwargs):
        """
        Checks if solicitud.solicitud_actuacion is correct.
        """
        verbosity = kwargs.get("verbosity", 1)
        dry_run = kwargs.get("dry_run", False)
        sqliteConnection = sqlite3.connect("/home/willy/dev/padron/padron/db.sqlite3")
        cursor = sqliteConnection.cursor()
        agente_padron = {}
        total = 0
        coincidentes = 0
        actualizados = 0
        no_encontrados = 0
        discrepancias = []
        for agente in Agente.objects.all():
            total += 1
            query = f'SELECT "listado_padron"."id", "listado_padron"."DISTRITO", "listado_padron"."TX_TIPO_EJEMPLAR", "listado_padron"."NU_MATRICULA", "listado_padron"."TX_APELLIDO", "listado_padron"."TX_NOMBRE", "listado_padron"."TX_CLASE", "listado_padron"."TX_GENERO", "listado_padron"."TX_DOMICILIO", "listado_padron"."TX_SECCION", "listado_padron"."TX_CIRCUITO", "listado_padron"."TX_LOCALIDAD", "listado_padron"."TX_CODIGO_POSTAL", "listado_padron"."TX_TIPO_NACIONALIDAD", "listado_padron"."NUMERO_MESA", "listado_padron"."NU_ORDEN_MESA" FROM "listado_padron" WHERE "listado_padron"."NU_MATRICULA" = {agente.dni}'
            cursor.execute(query)
            result = cursor.fetchall()
            try:
                agente_padron.update({
                "id":result[0][0],
                "provincia": result[0][1],
                "tipo_ejemplar": result[0][2],
                "dni": result[0][3],
                "apellido": result[0][4].title(),
                "nombres": result[0][5].title(),
                })
                nombreyapellido_padron = f"{agente_padron['apellido']}, {agente_padron['nombres']}"
                dni_padron = agente_padron['dni']
                nombreyapellido_carga = f"{agente.agente_apellidos}, {agente.agente_nombres}"
                dni_carga = agente.dni

                if f"{agente_padron['apellido']}, {agente_padron['nombres']}" != f"{agente.agente_apellidos}, {agente.agente_nombres}":
                    discrepancias.append({
                        "dni": dni_carga,
                        "carga": nombreyapellido_carga,
                        "padron": nombreyapellido_padron,
                    })
                    if verbosity >= 2:
                        self.stdout.write(f"{self.style.NOTICE('CARGA Y PADRON NO COINCIDEN:')}")
                        self.stdout.write(f"    Padron: {nombreyapellido_padron} - DNI: {dni_padron}")
                        self.stdout.write(f"    Carga: {nombreyapellido_carga} - DNI: {dni_carga}")
                    agente.agente_apellidos=agente_padron["apellido"]
                    agente.agente_nombres=agente_padron["nombres"]
                    agente.agente_verificado_contra_padron=True
                    if verbosity >= 2:
                        if dry_run:
                            self.stdout.write(f"{self.style.WARNING('[DRY-RUN] Se actualizaría nombre y apellidos...')}")
                        else:
                            self.stdout.write(f"{self.style.WARNING('Actualizando nombre y apellidos...')}")
                    if not dry_run:
                        agente.save()
                        time.sleep(0.01)
                    actualizados += 1
                    if verbosity >= 2:
                        self.stdout.write(f"{self.style.SUCCESS('OK.')}")
                        self.stdout.write(f"{'----------'*8}")
                else:
                    agente.agente_verificado_contra_padron=True
                    if not dry_run:
                        agente.save()
                    coincidentes += 1

            except IndexError:
                no_encontrados += 1
                if verbosity >= 1:
                    self.stdout.write(self.style.ERROR(f"Agente {agente.agente_apellidos}, {agente.agente_nombres} - {agente.dni}, no se encuentra en el padron"))

        if verbosity >= 1:
            self.stdout.write("")
            if dry_run:
                self.stdout.write(self.style.NOTICE("Modo dry-run: no se guardó ningún cambio en la base de datos."))
            self.stdout.write(self.style.MIGRATE_HEADING("Resumen:"))
            self.stdout.write(f"    Total de agentes verificados: {total}")
            self.stdout.write(self.style.SUCCESS(f"    Coincidentes (sin cambios): {coincidentes}"))
            self.stdout.write(self.style.WARNING(f"    Actualizados (padron != carga): {actualizados}"))
            self.stdout.write(self.style.ERROR(f"    No encontrados en el padron: {no_encontrados}"))

        if discrepancias and verbosity >= 1:
            self.stdout.write("")
            self.stdout.write(self.style.MIGRATE_HEADING("Discrepancias corregidas (carga -> padron):"))
            for d in discrepancias:
                self.stdout.write(f"    DNI {d['dni']}: {self.style.WARNING(d['carga'])} -> {self.style.SUCCESS(d['padron'])}")