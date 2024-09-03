from django.core.management.base import BaseCommand, CommandError
from secretariador.models import Solicitud, Comisionado
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
    def handle(self, *args, **kwargs):
        """
        Checks if solicitud.solicitud_actuacion is correct.
        """
        sqliteConnection = sqlite3.connect("/home/willy/dev/padron/padron/db.sqlite3")
        cursor = sqliteConnection.cursor()
        agente_padron = {}
        for agente in Comisionado.objects.all():
            query = f'SELECT "listado_padron"."id", "listado_padron"."DISTRITO", "listado_padron"."TX_TIPO_EJEMPLAR", "listado_padron"."NU_MATRICULA", "listado_padron"."TX_APELLIDO", "listado_padron"."TX_NOMBRE", "listado_padron"."TX_CLASE", "listado_padron"."TX_GENERO", "listado_padron"."TX_DOMICILIO", "listado_padron"."TX_SECCION", "listado_padron"."TX_CIRCUITO", "listado_padron"."TX_LOCALIDAD", "listado_padron"."TX_CODIGO_POSTAL", "listado_padron"."TX_TIPO_NACIONALIDAD", "listado_padron"."NUMERO_MESA", "listado_padron"."NU_ORDEN_MESA" FROM "listado_padron" WHERE "listado_padron"."NU_MATRICULA" = {agente.comisionado_dni}'
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
                nombreyapellido_carga = f"{agente.comisionado_apellidos}, {agente.comisionado_nombres}"
                dni_carga = agente.comisionado_dni

                if f"{agente_padron['apellido']}, {agente_padron['nombres']}" != f"{agente.comisionado_apellidos}, {agente.comisionado_nombres}":
                    self.stdout.write(f"{self.style.NOTICE('CARGA Y PADRON NO COINCIDEN:')}")
                    self.stdout.write(f"    Padron: {nombreyapellido_padron} - DNI: {dni_padron}")
                    self.stdout.write(f"    Carga: {nombreyapellido_carga} - DNI: {dni_carga}")
                    agente.comisionado_apellidos=agente_padron["apellido"]
                    agente.comisionado_nombres=agente_padron["nombres"]
                    agente.comisionado_verificado_contra_padron=True
                    self.stdout.write(f"{self.style.WARNING('Actualizando nombre y apellidos...')}")
                    agente.save()
                    time.sleep(0.01)
                    self.stdout.write(f"{self.style.SUCCESS('OK.')}")
                    self.stdout.write(f"{'----------'*8}")
                else:
                    # self.stdout.write(f"Padron: {nombreyapellido_padron} // Carga: {nombreyapellido_carga}")
                    agente.comisionado_verificado_contra_padron=True
                    agente.save()
                
                # print(agente.comisionado_nombreyapellido)
                
            except IndexError:
                self.stdout.write(self.style.ERROR(f"Agente {agente.comisionado_apellidos}, {agente.comisionado_nombres} - {agente.comisionado_dni}, no se encuentra en el padron"))