"""
ETL de la base GDU heredada (Hasura) a los modelos de gdu. Lee de una base scratch
donde se restauró el dump de Hasura (schemas public/our/audit, tal cual el dump) y
carga todo en una sola transacción: vacía las tablas de gdu, carga y resetea las
secuencias. Se puede correr tantas veces como haga falta; el corte final es una
corrida más contra el último dump.

Criterios (ver el plan del rediseño):
- se conservan las PKs heredadas;
- no se fusionan ni corrigen datos de negocio: lo dudoso se carga y queda como
  advertencia en el reporte; solo se descarta lo que no se puede cargar;
- las normalizaciones semánticas salen de los CSV versionados de gdu/etl/mapeos.
"""
import csv
import json
import re
import time
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ValidationError
from django.core.management.color import no_style
from django.db import connection, transaction
from django.utils import timezone
from psycopg2.extras import RealDictCursor

from carga.models import Localidad
from core.validators import CuitValidator
from gdu import models as m
from gdu.models.base import EstadoDominial, TipoResolucion
from gdu.reglas import ReglaInvalida, traducir_js

from .reporte import ADVERTENCIA, DESCARTE, Reporte

MAPEOS = Path(__file__).parent / "mapeos"
LOTE = 2000

ESTADO_DOMINIAL = {label: value for value, label in EstadoDominial.choices}
TIPO_RESOLUCION = {label: value for value, label in TipoResolucion.choices}
SI_NO = {"SI": True, "NO": False}
PLANO_TEXTO = re.compile(r"^\s*(\d{1,2})\s*/\s*(\d+)\s*/\s*(\w{1,2})\s*$")
SIN_DATO = {"", "sin dato", "s/d"}

# visualizador.role.nombre -> codename del permiso equivalente en gdu (Meta.permissions de
# los modelos; view_relevamiento lo genera Django). admin-user no tiene equivalente: la
# administración de usuarios pasa a ser la de polizador.
ROL_A_PERMISO = {
    "barrios-ver": "ver_barrios",
    "expropiaciones-ver": "ver_expropiaciones",
    "viviendas-ver": "ver_viviendas",
    "viviendas-dispersas-ver": "ver_viviendas_dispersas",
    "plano-mensura-ver": "ver_plano_mensura",
    "catastro-urbano-ver": "ver_catastro_urbano",
    "escriturar-ver": "ver_escriturar",
    "dominio-editar": "editar_dominio",
    "editar-nro_adjudicatario": "editar_nro_adjudicatario",
    "relevamiento-ver": "view_relevamiento",
    "relevamiento-encuestar": "encuestar_relevamiento",
}


class Rollback(Exception):
    """Se lanza al final de una corrida --dry-run para descartar la transacción."""


def _texto(valor):
    return "" if valor is None else valor


def _json(valor):
    # psycopg2 decodifica jsonb, salvo en la conexión de Django (que lo deja como texto)
    return json.loads(valor) if isinstance(valor, str) else valor


@contextmanager
def _sin_auto_now():
    # el ETL carga updated_at / enviada_en con los valores heredados
    campos = [
        f for modelo in apps.get_app_config("gdu").get_models() for f in modelo._meta.concrete_fields
        if getattr(f, "auto_now", False) or getattr(f, "auto_now_add", False)
    ]
    originales = [(f, f.auto_now, f.auto_now_add) for f in campos]
    for f in campos:
        f.auto_now = f.auto_now_add = False
    try:
        yield
    finally:
        for f, auto_now, auto_now_add in originales:
            f.auto_now, f.auto_now_add = auto_now, auto_now_add


class Importador:
    def __init__(self, dsn=None, log=print, conexion=None):
        # conexion: una conexión psycopg2 ya abierta (los tests leen el esquema heredado
        # desde la misma base y transacción de Django); si no, se abre una de solo lectura
        self._conexion_propia = conexion is None
        self.origen = psycopg2.connect(dsn) if conexion is None else conexion
        if self._conexion_propia:
            self.origen.set_session(readonly=True)
        self.reporte = Reporte()
        self.log = log
        self.ahora = timezone.now()
        self.cargados = defaultdict(set)
        self.usuarios_sin_mapear = Counter()
        self._destino = None
        self._id_actual = None

    # --- infraestructura ---

    def ejecutar(self, dry_run=False):
        inicio = time.monotonic()
        try:
            with transaction.atomic(), _sin_auto_now():
                self._vaciar()
                self._usuarios()
                self._preparar_mapeos()
                for paso in (
                    self._proyecto, self._adjudicatarios, self._territorio, self._planos, self._tierras,
                    self._expropiaciones, self._referencias, self._encuestas, self._auditoria_visor,
                ):
                    paso()
                # las FKs de Django son DEFERRABLE: se verifican acá, con el reporte a mano, y no
                # recién en el commit
                with connection.cursor() as cur:
                    cur.execute("SET CONSTRAINTS ALL IMMEDIATE")
                self._resetear_secuencias()
                self._notas_finales(time.monotonic() - inicio)
                if dry_run:
                    raise Rollback
        except Rollback:
            self.reporte.nota("Corrida --dry-run: la transacción se descartó, la base no cambió.")
        finally:
            if self._conexion_propia:
                self.origen.close()
        return self.reporte

    def _leer(self, sql):
        with self.origen.cursor(name="etl_gdu", cursor_factory=RealDictCursor) as cur:
            cur.itersize = LOTE
            cur.execute(sql)
            yield from cur

    def _consultar(self, sql):
        with self.origen.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def _cargar(self, origen, modelo, sql, convertir):
        """Lee `sql` de la base heredada, convierte cada fila con `convertir` (que devuelve
        una instancia, una lista de instancias o None si la descartó) y hace bulk_create."""
        self._destino = modelo._meta.db_table
        resumen = self.reporte.tabla(origen, self._destino)
        lote = []

        def volcar():
            objetos = modelo.objects.bulk_create(lote)
            resumen.cargadas += len(objetos)
            self.cargados[modelo].update(o.pk for o in objetos)
            lote.clear()

        for fila in self._leer(sql):
            resumen.leidas += 1
            self._id_actual = fila.get("id")
            resultado = convertir(fila)
            if resultado is None:
                continue
            lote.extend(resultado if isinstance(resultado, list) else [resultado])
            if len(lote) >= LOTE:
                volcar()
        if lote:
            volcar()
        self.log(f"  {modelo.__name__}: {resumen.cargadas} cargadas de {resumen.leidas} leídas")

    def _advertir(self, motivo, detalle=""):
        self.reporte.incidencia(self._destino, self._id_actual, ADVERTENCIA, motivo, str(detalle))

    def _descartar(self, motivo, detalle=""):
        self.reporte.incidencia(self._destino, self._id_actual, DESCARTE, motivo, str(detalle))

    def _requiere(self, **padres):
        """Descarta la fila si alguno de sus padres obligatorios no se cargó (fue descartado)."""
        for nombre, (modelo, pk) in padres.items():
            if pk not in self.cargados[modelo]:
                self._descartar(f"{nombre} no cargado", pk)
                return False
        return True

    def _vaciar(self):
        tablas = [
            connection.ops.quote_name(modelo._meta.db_table)
            for modelo in apps.get_app_config("gdu").get_models() if modelo._meta.managed
        ]
        with connection.cursor() as cur:
            cur.execute(f"TRUNCATE {', '.join(tablas)} RESTART IDENTITY")

    def _resetear_secuencias(self):
        modelos = list(apps.get_app_config("gdu").get_models())
        with connection.cursor() as cur:
            for sql in connection.ops.sequence_reset_sql(no_style(), modelos):
                cur.execute(sql)

    @staticmethod
    def _leer_csv(nombre, clave, valor):
        with open(MAPEOS / nombre, encoding="utf-8") as f:
            return {fila[clave].strip(): fila[valor].strip() for fila in csv.DictReader(f)}

    # --- conversiones comunes ---

    def _fecha(self, valor):
        if valor is None:
            return None
        return timezone.make_aware(valor) if timezone.is_naive(valor) else valor

    def _usuario(self, username):
        if not username:
            return None
        usuario_id = self.usuarios.get(username.strip().lower())
        if usuario_id is None:
            self.usuarios_sin_mapear[username.strip()] += 1
        return usuario_id

    def _auditoria(self, fila):
        return {
            "updated_at": self._fecha(fila.get("updated_at")) or self.ahora,
            "updated_by_id": self._usuario(fila.get("updated_by")),
        }

    def _geom(self, fila, obligatoria=True):
        """Geometría desde la columna geom_ewkb que agregan las consultas (ver _sql_geo)."""
        if fila["geom_ewkb"] is None:
            if obligatoria:
                self._descartar("sin geometría")
                return False
            return None
        if fila["geom_vacia"]:
            self._advertir("geometría vacía")
        elif not fila["geom_valida"]:
            self._advertir("geometría inválida (ST_IsValid)", fila["geom_razon"])
        return GEOSGeometry(memoryview(fila["geom_ewkb"]))

    @staticmethod
    def _sql_geo(tabla, transformar_a=None, extra=""):
        geom = f"ST_Transform(t.geom, {transformar_a})" if transformar_a else "t.geom"
        return (
            f"SELECT t.*, ST_AsEWKB({geom}) AS geom_ewkb, ST_IsValid(t.geom) AS geom_valida, "
            f"ST_IsEmpty(t.geom) AS geom_vacia, "
            f"CASE WHEN NOT ST_IsValid(t.geom) THEN ST_IsValidReason(t.geom) END AS geom_razon "
            f"FROM {tabla} t {extra} ORDER BY t.{'gid' if tabla.endswith('zonas_parcelas') else 'id'}"
        )

    def _localidad(self, id_legacy, obligatoria=True):
        if id_legacy is None:
            return None
        localidad_id = self.localidades.get(id_legacy)
        if localidad_id is None:
            (self._descartar if obligatoria else self._advertir)("localidad sin equivalente en carga", id_legacy)
            return False if obligatoria else None
        return localidad_id

    def _estado_dominial(self, valor):
        if valor is None:
            return ""
        estado = ESTADO_DOMINIAL.get(valor)
        if estado is None:
            self._advertir("estado dominial desconocido", valor)
            return ""
        return estado

    def _datos_adjudicatario(self, fila):
        """Separa el nro_adjudicatario polimórfico heredado en dni / adjudicatario."""
        nro, tipo = fila["nro_adjudicatario"], fila["tipo_id_adjudicatario"]
        if nro is None:
            return {}
        if nro in self.nros_repetidos[self._destino]:
            self._advertir("nro_adjudicatario repetido en otra fila", nro)
        if tipo == "DNI":
            return {"dni": nro}
        if tipo == "NRO ADJUDICATARIO" or nro in self.cargados[m.Adjudicatario3450]:
            if nro not in self.cargados[m.Adjudicatario3450]:
                self._advertir("adjudicatario inexistente en Sistema 3450", nro)
            return {"adjudicatario_id": nro}
        self._advertir("nro_adjudicatario sin tipo ni coincidencia en Sistema 3450", nro)
        return {"nro_adjudicatario_legacy": nro}

    # --- usuarios ---

    def _usuarios(self):
        """Cuentas y roles de visualizador.* -> CustomUser + Groups. Las contraseñas no se
        copian: las cuentas nuevas quedan con contraseña inutilizable y entran por LDAP
        (core.ldap_backend adopta la cuenta por username). Si el username ya existe en
        polizador se reutiliza esa cuenta. No se vacía nada: es get-or-create."""
        self.log("Usuarios y roles")
        User = get_user_model()
        self._destino = "auth_group"
        self.reporte.tabla("visualizador.role", self._destino)
        permisos = {p.codename: p for p in Permission.objects.filter(content_type__app_label="gdu")}
        grupos = {}
        for id_rol, nombre in self._consultar("SELECT id, nombre FROM visualizador.role ORDER BY id"):
            self._id_actual = id_rol
            self.reporte.tablas[self._destino].leidas += 1
            permiso = permisos.get(ROL_A_PERMISO.get(nombre))
            if permiso is None:
                self._descartar("rol sin permiso equivalente en gdu", nombre)
                continue
            grupo, _ = Group.objects.get_or_create(name=f"GDU: {nombre}")
            grupo.permissions.set([permiso])
            grupos[id_rol] = grupo
            self.reporte.tablas[self._destino].cargadas += 1

        self._destino = User._meta.db_table
        resumen = self.reporte.tabla("visualizador.user", self._destino)
        usuarios, creados = {}, 0
        existentes = {u.username.lower(): u for u in User.objects.all()}
        for id_usuario, username, nombre, activo, creado in self._consultar(
            'SELECT id, username, nombre, activo, created_at FROM visualizador."user" ORDER BY id'
        ):
            self._id_actual = id_usuario
            resumen.leidas += 1
            usuario = existentes.get(username.strip().lower())
            if usuario is None:
                usuario = User(
                    username=username.strip(), first_name=nombre or "", is_active=bool(activo),
                    date_joined=self._fecha(creado) or self.ahora,
                )
                usuario.set_unusable_password()
                usuario.save()
                existentes[usuario.username.lower()] = usuario
                creados += 1
            usuarios[id_usuario] = usuario
            resumen.cargadas += 1

        asignaciones = 0
        for id_usuario, id_rol in self._consultar('SELECT "user", role FROM visualizador.rolemapping'):
            if id_rol in grupos and id_usuario in usuarios:
                usuarios[id_usuario].groups.add(grupos[id_rol])
                asignaciones += 1
        self.reporte.nota(
            f"Usuarios: {creados} creados, {len(usuarios) - creados} ya existían; "
            f"{len(grupos)} grupos GDU, {asignaciones} asignaciones usuario-grupo"
        )
        self.log(f"  {creados} usuarios creados, {len(usuarios) - creados} reutilizados, {asignaciones} asignaciones")

    # --- mapeos previos ---

    def _preparar_mapeos(self):
        User = get_user_model()
        self.usuarios = {
            username.lower(): pk for pk, username in User.objects.values_list("pk", User.USERNAME_FIELD)
        }

        ids_carga = set(Localidad.objects.values_list("pk", flat=True))
        excepciones = {int(k): int(v) for k, v in self._leer_csv("localidad.csv", "id_legacy", "id_carga").items()}
        self.localidades = {}
        for id_legacy, codpcia, coddpto, codloc, nombre in self._consultar(
            "SELECT id, codpcia, coddpto, codloc, localidad FROM public.localidad"
        ):
            codigo = excepciones.get(id_legacy) or int(f"{codpcia.strip()}{coddpto.strip()}{codloc.strip()}")
            if codigo in ids_carga:
                self.localidades[id_legacy] = codigo
            else:
                self.reporte.nota(f"Localidad heredada {id_legacy} ({nombre}, INDEC {codigo}) sin equivalente en carga")

        self.nros_repetidos = {}
        for tabla, modelo in (("uf", m.Uf), ("vivienda_punto", m.ViviendaPunto)):
            self.nros_repetidos[modelo._meta.db_table] = {
                nro for (nro,) in self._consultar(
                    f"SELECT nro_adjudicatario FROM public.{tabla} WHERE nro_adjudicatario IS NOT NULL "
                    f"GROUP BY 1 HAVING count(*) > 1"
                )
            }

    # --- pasos ---

    def _lookup(self, tabla, modelo):
        self._cargar(
            f"public.{tabla}", modelo, f"SELECT * FROM public.{tabla} ORDER BY id",
            lambda f: modelo(id=f["id"], nombre=f["nombre"], **self._auditoria(f)),
        )

    def _proyecto(self):
        self.log("Proyecto (programa → intervención, ejecutores)")
        origenes = self._leer_csv("programa_origen.csv", "valor_legacy", "origen")

        def programa(f):
            valor = (f["origen"] or "").strip()
            if valor and valor not in origenes:
                self._advertir("origen sin mapeo en programa_origen.csv", valor)
            return m.Programa(id=f["id"], nombre=f["nombre"], origen=origenes.get(valor, ""), **self._auditoria(f))

        self._cargar("public.programa", m.Programa, "SELECT * FROM public.programa ORDER BY id", programa)

        def actuacion(f):
            if not self._requiere(programa=(m.Programa, f["id_programa"])):
                return None
            return m.Actuacion(
                id=f["id"], programa_id=f["id_programa"], ano=f["ano"], nombre=f["nombre"],
                instrumento=f["instrumento"], **self._auditoria(f),
            )

        self._cargar("public.actuacion", m.Actuacion, "SELECT * FROM public.actuacion ORDER BY id", actuacion)
        self._lookup("tipo_contratacion", m.TipoContratacion)

        def contratacion(f):
            if not self._requiere(actuacion=(m.Actuacion, f["id_actuacion"])):
                return None
            return m.Contratacion(
                id=f["id"], actuacion_id=f["id_actuacion"], tipo_id=f["tipo"], expediente=_texto(f["expediente"]),
                resolucion=_texto(f["resolucion"]), ano=f["ano"], nombre=_texto(f["nombre"]), **self._auditoria(f),
            )

        self._cargar("public.contratacion", m.Contratacion, "SELECT * FROM public.contratacion ORDER BY id", contratacion)
        self._lookup("tipo_intervencion", m.TipoIntervencion)

        def adjudicacion(f):
            return m.AdjudicacionBeneficiario(
                id=f["id"], nro=f["nro"], ano=f["ano"], tipo=TIPO_RESOLUCION[f["tipo"]], **self._auditoria(f),
            )

        self._cargar(
            "public.adjudicacion_beneficiario", m.AdjudicacionBeneficiario,
            "SELECT * FROM public.adjudicacion_beneficiario ORDER BY id", adjudicacion,
        )

        def resolucion(f):
            return m.ResolucionCostos(
                id=f["id"], nro_largo=f["nro_largo"], nro_corto=f["nro_corto"], ano=f["ano"],
                tipo=TIPO_RESOLUCION[f["tipo"]], **self._auditoria(f),
            )

        self._cargar("public.resolucion_costos", m.ResolucionCostos, "SELECT * FROM public.resolucion_costos ORDER BY id", resolucion)

        estados = {}
        for id_estado, nombre in self._consultar("SELECT id, nombre FROM public.tipo_estado"):
            nombre = nombre.strip().lower()
            if nombre.startswith("evalu"):
                estados[id_estado] = m.Intervencion.Estado.EVALUACION
            elif nombre.startswith("termin"):
                estados[id_estado] = m.Intervencion.Estado.TERMINADA

        def intervencion(f):
            localidad = self._localidad(f["id_localidad"])
            if localidad is False or not self._requiere(contratacion=(m.Contratacion, f["id_contratacion"])):
                return None
            estado = estados.get(f["estado"], "")
            if f["estado"] is not None and not estado:
                self._advertir("estado sin equivalente", f["estado"])
            grupo = (f["grupo"] or "").strip()
            if f["drf_grupo"] is not None:
                if not grupo:
                    grupo = str(f["drf_grupo"])
                elif grupo.isdigit() and int(grupo) != f["drf_grupo"]:
                    self._advertir("grupo y drf_grupo no coinciden", f"{grupo} / {f['drf_grupo']}")
            return m.Intervencion(
                id=f["id"], contratacion_id=f["id_contratacion"], localidad_id=localidad, nombre=f["nombre"],
                tipo_id=f["tipo"], estado=estado, avance=f["avance"], plan=f["drf_plan"], grupo=grupo,
                adjudicacion_id=f["id_adjudicacion"], **self._auditoria(f),
            )

        self._cargar("public.intervencion", m.Intervencion, "SELECT * FROM public.intervencion ORDER BY id", intervencion)
        self._lookup("tipo_ejecutor", m.TipoEjecutor)
        validar_cuit = CuitValidator()

        def ejecutor(f):
            cuit = (f["cuit"] or "").strip()
            try:
                validar_cuit(cuit)
            except ValidationError:
                self._advertir("CUIT inválido", cuit)
            return m.Ejecutor(
                id=f["id"], tipo_id=f["tipo"], cuit=cuit, nombre=f["nombre"],
                localidad_id=self._localidad(f["id_localidad"], obligatoria=False),
                nombre_contacto=_texto(f["nombre_contacto"]), **self._auditoria(f),
            )

        self._cargar("public.ejecutor", m.Ejecutor, "SELECT * FROM public.ejecutor ORDER BY id", ejecutor)
        self._lookup("inspector", m.Inspector)
        self._nn(
            "public.intervencion_ejecutor", m.IntervencionEjecutor, "id_intervencion", "id_ejecutor",
            ("intervencion", m.Intervencion), ("ejecutor", m.Ejecutor),
        )
        self._nn(
            "public.intervencion_inspector", m.IntervencionInspector, "idintervencion", "idinspector",
            ("intervencion", m.Intervencion), ("inspector", m.Inspector),
        )

    def _nn(self, origen, modelo, col_a, col_b, padre_a, padre_b, col_tipo=None):
        """Tablas N:N: los pares repetidos (idénticos) se descartan, quedan una sola vez."""
        vistos = set()

        def convertir(f):
            clave = (f[col_a], f[col_b], f[col_tipo] if col_tipo else None)
            if clave in vistos:
                self._descartar("par duplicado", clave[:2])
                return None
            if not self._requiere(**{padre_a[0]: (padre_a[1], f[col_a]), padre_b[0]: (padre_b[1], f[col_b])}):
                return None
            vistos.add(clave)
            campos = {f"{padre_a[0]}_id": f[col_a], f"{padre_b[0]}_id": f[col_b]}
            if col_tipo:
                campos["tipo"] = f[col_tipo]
            return modelo(id=f["id"], **campos, **self._auditoria(f))

        self._cargar(origen, modelo, f"SELECT * FROM {origen} ORDER BY id", convertir)

    def _adjudicatarios(self):
        self.log("Adjudicatarios del Sistema 3450")

        def adjudicatario(f):
            self._id_actual = f["AdjuGISNroAdju"]
            escritura = (f["AdjuGISEscritura"] or "").strip().upper()
            if escritura and escritura not in SI_NO:
                self._advertir("escritura con valor desconocido", escritura)
            return m.Adjudicatario3450(
                nro_adjudicatario=f["AdjuGISNroAdju"], apellido_nombre=_texto(f["AdjuGISapeynom"]).strip(),
                dni=f["AdjuGISdni"], direccion=_texto(f["AdjuGISdireccion"]).strip(),
                escritura=SI_NO.get(escritura), matricula=_texto(f["AdjuGISmatricula"]).strip(),
                res_nro=f["AdjuGISResNro"], res_fecha=f["AdjuGISResFecha"], res_acta=_texto(f["AdjuGISResActa"]),
                motivo=_texto(f["AdjuGISmotivo"]), situacion=_texto(f["AdjuGISsituacion"]).strip(),
                estado_regularizacion=_texto(f["estado_regularizacion"]), actualizado_en=self.ahora,
            )

        self._cargar(
            "public.adjudicatario3450 + tmp_regularizacion", m.Adjudicatario3450,
            'SELECT a.*, r.estado AS estado_regularizacion FROM public.adjudicatario3450 a '
            'LEFT JOIN public.tmp_regularizacion r ON r.nro_adjudicatario = a."AdjuGISNroAdju" '
            'ORDER BY a."AdjuGISNroAdju"',
            adjudicatario,
        )
        (huerfanos,) = self._consultar(
            'SELECT count(*) FROM public.tmp_regularizacion r WHERE NOT EXISTS '
            '(SELECT 1 FROM public.adjudicatario3450 a WHERE a."AdjuGISNroAdju" = r.nro_adjudicatario)'
        )[0]
        if huerfanos:
            self.reporte.nota(f"tmp_regularizacion: {huerfanos} filas sin adjudicatario en 3450 (no se cargan)")

    def _territorio(self):
        self.log("Territorio (barrios, parcelas, UF, viviendas)")
        for tabla, modelo in (("barrio", m.Barrio), ("manzana", m.Manzana), ("calle", m.Calle)):
            def convertir(f, modelo=modelo):
                geom = self._geom(f)
                if geom is False or not self._requiere(intervencion=(m.Intervencion, f["id_intervencion"])):
                    return None
                return modelo(
                    id=f["id"], intervencion_id=f["id_intervencion"], nombre=_texto(f["nombre"]), geom=geom,
                    **self._auditoria(f),
                )

            self._cargar(f"public.{tabla}", modelo, self._sql_geo(f"public.{tabla}"), convertir)

        self._lookup("destino_parcela", m.DestinoParcela)
        nomenclaturas_repetidas = {
            n for (n,) in self._consultar(
                "SELECT nomenclatura FROM public.parcela WHERE nomenclatura IS NOT NULL GROUP BY 1 HAVING count(*) > 1"
            )
        }

        def parcela(f):
            geom = self._geom(f)
            if geom is False or not self._requiere(intervencion=(m.Intervencion, f["id_intervencion"])):
                return None
            if f["nomenclatura"] in nomenclaturas_repetidas:
                self._advertir("nomenclatura repetida en otra parcela", f["nomenclatura"])
            return m.Parcela(
                id=f["id"], intervencion_id=f["id_intervencion"], destino_id=f["destino"],
                estado_dominial=self._estado_dominial(f["estado_dominial"]), geom=geom,
                **self._nomenclatura(f), **self._auditoria(f),
            )

        self._cargar("public.parcela", m.Parcela, self._sql_geo("public.parcela"), parcela)

        def uf(f):
            geom = self._geom(f)
            if geom is False or not self._requiere(parcela=(m.Parcela, f["id_parcela"])):
                return None
            return m.Uf(
                id=f["id"], parcela_id=f["id_parcela"], uf=f["uf"], poligono=_texto(f["poligono"]),
                coefuf=f["coefuf"], nivel=f["nivel"], designacion=_texto(f["designacion"]),
                estado_dominial=self._estado_dominial(f["estado_dominial"]), fr_mat=_texto(f["fr_mat"]),
                res_costos_id=f["res_costos"], observaciones=_texto(f["observaciones"]), geom=geom,
                **self._datos_adjudicatario(f), **self._auditoria(f),
            )

        self._cargar("public.uf", m.Uf, self._sql_geo("public.uf"), uf)

        def vivienda_punto(f):
            geom = self._geom(f)
            if geom is False or not self._requiere(intervencion=(m.Intervencion, f["id_intervencion"])):
                return None
            return m.ViviendaPunto(
                id=f["id"], intervencion_id=f["id_intervencion"],
                estado_dominial=self._estado_dominial(f["estado_dominial"]), apellido=_texto(f["apellido"]),
                nombre=_texto(f["nombre"]), geom=geom, **self._nomenclatura(f), **self._datos_adjudicatario(f),
                **self._auditoria(f),
            )

        self._cargar("public.vivienda_punto", m.ViviendaPunto, self._sql_geo("public.vivienda_punto"), vivienda_punto)

    @staticmethod
    def _nomenclatura(fila):
        # las partes heredadas son char(n): Postgres descartaba el relleno al concatenarlas
        # en set_nomenclatura(), así que se recorta para obtener la misma nomenclatura
        return {
            campo: None if fila[campo] is None else fila[campo].rstrip()
            for campo in ("dpto", "circ", "secc", "ch", "qta", "fracc", "mz", "parc")
        }

    def _planos(self):
        self.log("Planos de mensura")
        self.planos_por_ident = defaultdict(list)

        def plano(f):
            geom = self._geom(f, obligatoria=False)
            self.planos_por_ident[(f["depto"].strip().zfill(2), f["nro"], f["ano"].strip())].append(f["id"])
            return m.PlanoMensura(
                id=f["id"], depto=f["depto"], nro=f["nro"], ano=f["ano"], pm_antecedente=_texto(f["pm_antecedente"]),
                en_gdu=f["en_gdu"], sup_parcelas=f["sup_parcelas"], sup_calles=f["sup_calles"],
                sup_reserva=f["sup_reserva"], geom=geom, **self._auditoria(f),
            )

        self._cargar("public.plano_mensura", m.PlanoMensura, self._sql_geo("public.plano_mensura"), plano)
        repetidos = sum(1 for ids in self.planos_por_ident.values() if len(ids) > 1)
        if repetidos:
            self.reporte.nota(f"plano_mensura: {repetidos} identificadores (depto, nro, año) repetidos")
        self._nn(
            "public.plano_mensura_intervencion", m.PlanoMensuraIntervencion, "idplano", "idintervencion",
            ("plano", m.PlanoMensura), ("intervencion", m.Intervencion), col_tipo="tipo",
        )

        def pre_adjudicatario(f):
            geom = self._geom(f)
            if geom is False:
                return None
            texto_plano = (f["plano_mensura"] or "").strip()
            plano_id, plano_legacy = None, ""
            if texto_plano.lower() not in SIN_DATO:
                coincidencia = PLANO_TEXTO.match(texto_plano)
                ids = []
                if coincidencia:
                    depto, nro, ano = coincidencia.groups()
                    ids = self.planos_por_ident.get((depto.zfill(2), int(nro), ano), [])
                if len(ids) == 1:
                    plano_id = ids[0]
                else:
                    plano_legacy = texto_plano
                    self._advertir("plano de mensura no resuelto", texto_plano)
            return m.PreAdjudicatarioDispersa(
                id=f["id"], apellido=f["apellido"], nombre=f["nombre"], genero=_texto(f["genero"]),
                documento=f["documento"], cantidad_personas=f["cantidad_personas"],
                inscripcion=_texto(f["inscripcion"]), plano_mensura_id=plano_id, plano_mensura_legacy=plano_legacy,
                propietario=_texto(f["propietario"]), apto_dominial=_texto(f["apto_dominial"]),
                observaciones=_texto(f["observaciones"]), geom=geom, **self._nomenclatura(f),
                updated_at=self.ahora,
            )

        self._cargar(
            "public.pre_adjudicatario_dispersa", m.PreAdjudicatarioDispersa,
            self._sql_geo("public.pre_adjudicatario_dispersa"), pre_adjudicatario,
        )

    def _tierras(self):
        self.log("Tierras")
        self._lookup("tierra_destino", m.TierraDestino)
        self._lookup("tipo_doc_probatoria", m.TipoDocProbatoria)

        def tierra(f):
            geom = self._geom(f)
            if geom is False:
                return None
            return m.Tierra(
                id=f["id"], tipo=f["tipo"], tipo_oferente=f["tipo_oferente"], oferente=_texto(f["oferente"]),
                propietario=_texto(f["propietario"]), localidad_id=self._localidad(f["localidad"], obligatoria=False),
                tipo_inscripcion=_texto(f["tipo_inscripcion"]), inscripcion=_texto(f["inscripcion"]),
                tipo_doc_probatoria_id=f["tipo_doc_probatoria"], apto_fisico=f["apto_fisico"],
                apto_dominial=f["apto_dominial"], apto_localizacion=f["apto_localizacion"],
                visita_campo=f["visita_campo"], visita_profesional=_texto(f["visita_profesional"]),
                visita_fecha=f["visita_fecha"], localizacion=_texto(f["localizacion"]),
                superficie=_texto(f["superficie"]), proyecto_loteo=f["proyecto_loteo"], estado=_texto(f["estado"]),
                destino_id=f["destino"], otro_destino=_texto(f["otro_destino"]).strip(),
                observaciones=_texto(f["observaciones"]), geom=geom, **self._nomenclatura(f), **self._auditoria(f),
            )

        self._cargar("public.tierra", m.Tierra, self._sql_geo("public.tierra"), tierra)

        def consultas(f):
            if f["id"] not in self.cargados[m.Tierra]:
                return None
            objetos = []
            for area in m.TierraConsulta.Area.values:
                valores = {
                    campo: f.get(f"{area}_{campo}")
                    for campo in ("solicitado", "respuesta", "resolucion", "observaciones", "valor")
                }
                if not any(v not in (None, "") and str(v).strip() for v in valores.values()):
                    continue
                objetos.append(m.TierraConsulta(
                    tierra_id=f["id"], area=area, valor=valores.pop("valor"),
                    **{k: _texto(v).strip() for k, v in valores.items()}, **self._auditoria(f),
                ))
            return objetos

        self._cargar("public.tierra (columnas por área)", m.TierraConsulta, "SELECT * FROM public.tierra ORDER BY id", consultas)

    def _expropiaciones(self):
        self.log("Expropiaciones")
        self._lookup("estado_gestion_expropiacion", m.EstadoGestionExpropiacion)
        self._lookup("objeto_expropiacion", m.ObjetoExpropiacion)
        gestiones = {"Ipduv": m.Expropiacion.Gestion.IPDUV, "Externa": m.Expropiacion.Gestion.EXTERNA}

        def expropiacion(f):
            localidad = self._localidad(f["localidad"])
            if localidad is False:
                return None
            return m.Expropiacion(
                id=f["id"], nro_ley=f["nro_ley"], letra_ley=(f["letra_ley"] or "").strip(), ano_ley=f["ano_ley"],
                ley_prorrogas=_texto(f["ley_prorrogas"]), localidad_id=localidad, asentamiento=f["asentamiento"],
                asentamiento_nombre=_texto(f["asentamiento_nombre"]), gestion=gestiones[f["gestion"]],
                **self._auditoria(f),
            )

        self._cargar("public.expropiacion", m.Expropiacion, "SELECT * FROM public.expropiacion ORDER BY id", expropiacion)

        def parcela_expropiada(f):
            geom = self._geom(f)
            if geom is False or not self._requiere(expropiacion=(m.Expropiacion, f["id_expropiacion"])):
                return None
            regularizable = (f["regularizable"] or "").strip().upper()
            if regularizable and regularizable not in SI_NO:
                self._advertir("regularizable con valor desconocido", regularizable)
            return m.ParcelaExpropiada(
                id=f["id"], expropiacion_id=f["id_expropiacion"], objeto_id=f["objeto"],
                estado_gestion_id=f["estado_gestion"], propietario_expropiado=_texto(f["propietario_expropiado"]),
                propietario_actual=_texto(f["propietario_actual"]), inscripcion=_texto(f["inscripcion"]),
                regularizable=SI_NO.get(regularizable), observaciones=_texto(f["observaciones"]), geom=geom,
                **self._nomenclatura(f), **self._auditoria(f),
            )

        self._cargar("public.parcela_expropiada", m.ParcelaExpropiada, self._sql_geo("public.parcela_expropiada"), parcela_expropiada)

    def _referencias(self):
        self.log("Capas de referencia (catastro urbano, zonas)")

        def catastro(f):
            return m.Catastrourbano(
                id=f["id"], geom=self._geom(f, obligatoria=False), tomo=f["tomo"], folio=f["folio"],
                finca=f["finca"], anio=f["anio"],
                **{c: _texto(f[c]) for c in (
                    "id_nomencl", "plano_apro", "dpto", "circ", "secc", "ch", "qta", "fracc", "mz", "parc", "matric",
                    "municipio",
                )},
            )

        self._cargar("public.catastrourbano", m.Catastrourbano, self._sql_geo("public.catastrourbano"), catastro)

        def zona(f):
            self._id_actual = f["gid"]
            geom = self._geom(f)
            if geom is False:
                return None
            return m.ZonaParcelas(id=f["gid"], nombre=_texto(f["nombre"]), geom=geom)

        self._cargar("public.zonas_parcelas", m.ZonaParcelas, self._sql_geo("public.zonas_parcelas"), zona)

    def _regla(self, texto):
        try:
            return traducir_js(texto)
        except ReglaInvalida as e:
            self._advertir("regla JS no traducible (queda sin regla)", f"{e}: {texto}")
            return None

    def _encuestas(self):
        self.log("Encuestas")
        self._cargar(
            "our.tipo_pregunta", m.TipoPregunta, "SELECT * FROM our.tipo_pregunta ORDER BY id",
            lambda f: m.TipoPregunta(id=f["id"], nombre=f["nombre"], tipo=f["tipo"], descripcion=_texto(f["descripcion"])),
        )
        self._cargar(
            "our.relevamiento", m.Relevamiento, "SELECT id, nombre, fecha, descripcion, objetivo FROM our.relevamiento ORDER BY id",
            lambda f: m.Relevamiento(
                id=f["id"], nombre=f["nombre"], fecha=f["fecha"], descripcion=_texto(f["descripcion"]),
                objetivo=f["objetivo"],
            ),
        )
        self._cargar(
            "our.seccion", m.Seccion, "SELECT * FROM our.seccion ORDER BY id",
            lambda f: m.Seccion(
                id=f["id"], relevamiento_id=f["relevamiento"], nombre=f["nombre"], texto=_texto(f["texto"]),
                orden=f["orden"], regla_visible=self._regla(f["visible"]),
            ),
        )
        self._cargar(
            "our.pregunta", m.Pregunta, "SELECT * FROM our.pregunta ORDER BY id",
            lambda f: m.Pregunta(id=f["id"], tipo_id=f["tipo"], texto=f["texto"], subtexto=_texto(f["subtexto"])),
        )
        self._cargar(
            "our.pregunta_relevamiento", m.PreguntaRelevamiento, "SELECT * FROM our.pregunta_relevamiento ORDER BY id",
            lambda f: m.PreguntaRelevamiento(
                id=f["id"], relevamiento_id=f["relevamiento"], seccion_id=f["seccion"], pregunta_id=f["pregunta"],
                variable=f["variable"], regla_visible=self._regla(f["visible"]),
                regla_valido=self._regla(f["valido"]), requerida=f["required"],
            ),
        )
        self._cargar(
            "our.respuesta", m.Respuesta, "SELECT * FROM our.respuesta ORDER BY id",
            lambda f: m.Respuesta(
                id=f["id"], pregunta_id=f["pregunta"], texto=f["texto"], nro_opcion=f["nro_opcion"], valor=f["valor"],
            ),
        )

        viviendas = {}

        def vivienda(f):
            geom = self._geom(f)
            if geom is False:
                return None
            uf_id = f["vivienda"] if f["vivienda"] in self.cargados[m.Uf] else None
            if uf_id is None:
                self._advertir("vivienda sin UF correspondiente", f["vivienda"])
            viviendas[(f["relevamiento"], f["vivienda"])] = f["id"]
            datos = dict(_json(f["properties"]) or {})
            datos.pop("relevado", None)  # se deriva de las encuestas
            return m.ViviendaRelevamiento(
                id=f["id"], relevamiento_id=f["relevamiento"], numero=f["vivienda"], uf_id=uf_id, datos=datos, geom=geom,
            )

        self._cargar("our.vivienda", m.ViviendaRelevamiento, self._sql_geo("our.vivienda", transformar_a=m.base.SRID_GDU), vivienda)
        tipos_encuesta = set(m.Encuesta.Tipo.values)

        def encuesta(f):
            vivienda_id = viviendas.get((f["relevamiento"], f["vivienda"]))
            if vivienda_id is None:
                self._descartar("vivienda del relevamiento inexistente", f["vivienda"])
                return None
            tipo = f["tipo"]
            if tipo is not None and tipo not in tipos_encuesta:
                self._advertir("tipo de encuesta desconocido", tipo)
                tipo = None
            usuario_id = self._usuario(f["user"])
            fecha = self._fecha(f["tstamp"])
            return m.Encuesta(
                id=f["id"], relevamiento_id=f["relevamiento"], vivienda_id=vivienda_id, usuario_id=usuario_id,
                usuario_legacy="" if usuario_id else _texto(f["user"]), tipo=tipo, capturada_en=fecha,
                enviada_en=fecha or self.ahora,
            )

        self._cargar("our.encuesta", m.Encuesta, "SELECT * FROM our.encuesta ORDER BY id", encuesta)

        def respuesta_encuesta(f):
            if not self._requiere(encuesta=(m.Encuesta, f["encuesta"])):
                return None
            return m.RespuestaEncuesta(
                id=f["id"], encuesta_id=f["encuesta"], pregunta_relevamiento_id=f["pregunta"],
                respuesta_id=f["respuesta"], valor=f["valor"],
            )

        self._cargar("our.respuesta_encuesta", m.RespuestaEncuesta, "SELECT * FROM our.respuesta_encuesta ORDER BY id", respuesta_encuesta)

    def _auditoria_visor(self):
        self.log("Eventos del visor")

        def evento(f):
            return m.EventoVisor(
                id=f["id"], tstamp=self._fecha(f["tstamp"]), usuario_id=self.usuarios.get((f["username"] or "").lower()),
                username=_texto(f["username"]), accion=f["action"], ip=f["client_addr"], metadata=_json(f["metadata"]),
                importado=True,
            )

        self._cargar("audit.audit_logs", m.EventoVisor, "SELECT * FROM audit.audit_logs ORDER BY id", evento)

    def _notas_finales(self, segundos):
        if self.usuarios_sin_mapear:
            top = ", ".join(f"{u} ({n})" for u, n in self.usuarios_sin_mapear.most_common(10))
            self.reporte.nota(
                f"{len(self.usuarios_sin_mapear)} usernames heredados (updated_by / encuesta.user) sin usuario en "
                f"polizador; updated_by queda vacío. Más frecuentes: {top}"
            )
        self.reporte.nota("El historial (simple_history) arranca vacío: la carga inicial no genera registros.")
        self.reporte.nota(f"Duración: {segundos:.0f} s")
