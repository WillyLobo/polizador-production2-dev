#!/usr/bin/env bash
#
# Migra los datos de GDU (catastro / encuestas / visualizador / vistas / audit)
# desde un dump completo (databases/db-schema.sql del repo hasura) hacia la base
# de datos de polizador, en schemas propios, sin tocar ninguna tabla existente
# de polizador. Reproduce paso a paso el procedimiento validado manualmente en
# desarrollo contra polizadordbdev.
#
# Requisitos:
#   - Correr EN el servidor de Postgres de producción (o por un operador con
#     acceso de superusuario a esa base), porque dos pasos necesitan
#     `sudo -u postgres psql` para crear las extensiones postgis/pgcrypto.
#   - El paquete de sistema de PostGIS (ej. postgresql-<version>-postgis-3) ya
#     tiene que estar instalado — este script NO instala paquetes del SO, solo
#     verifica que la extensión esté disponible y aborta con instrucciones si no.
#   - El usuario de base (DBUSER, tomado del .env de polizador) necesita permiso
#     CREATEDB (para la base scratch temporal) además de sus permisos habituales.
#   - Es IDEMPOTENTE respecto a re-ejecuciones destructivas: aborta de entrada si
#     el schema 'catastro' ya existe en la base de destino, para no duplicar datos.
#
# Uso:
#   DUMP_FILE=/ruta/a/db-schema.sql ./migrar_gdu_a_produccion.sh
#
# Las credenciales de conexión (DBHOST/DBUSER/DBNAME/DBPASSWORD) se leen por
# default de polizador/.env (el .env real de producción del servidor donde se
# corra esto) y se pueden sobreescribir con variables de entorno.

set -euo pipefail

# --- Configuración ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ENV_FILE:-$SCRIPT_DIR/polizador/.env}"

: "${DUMP_FILE:?Definí DUMP_FILE con la ruta al db-schema.sql a importar}"
SCRATCH_DB="${SCRATCH_DB:-gdu_migracion_scratch}"
BACKUP_DIR="${BACKUP_DIR:-$SCRIPT_DIR/backups}"
SCHEMAS_GDU=(catastro our visualizador vistas audit)

log() { echo -e "\n>>> $*"; }
die() { echo "ERROR: $*" >&2; exit 1; }

# --- Credenciales: .env de polizador, salvo que ya vengan por variable de entorno ---
# (solo completa las que no estén seteadas desde afuera, para que las variables
# de entorno tengan siempre prioridad sobre el .env)
if [[ -f "$ENV_FILE" ]]; then
  while IFS='=' read -r key value; do
    if [[ -z "${!key:-}" ]]; then
      export "$key=$value"
    fi
  done < <(grep -E '^(DBHOST|DBUSER|DBNAME|DBPASSWORD)=' "$ENV_FILE")
fi

: "${DBHOST:?Falta DBHOST (host de Postgres de destino)}"
: "${DBUSER:?Falta DBUSER}"
: "${DBNAME:?Falta DBNAME (base de polizador de destino)}"
: "${DBPASSWORD:?Falta DBPASSWORD}"

export PGPASSWORD="$DBPASSWORD"
PSQL=(psql -U "$DBUSER" -h "$DBHOST" -v ON_ERROR_STOP=0)
PSQL_TARGET=(psql -U "$DBUSER" -h "$DBHOST" -d "$DBNAME" -v ON_ERROR_STOP=0)

# --- Chequeos previos ---
command -v psql >/dev/null || die "psql no está instalado"
command -v pg_dump >/dev/null || die "pg_dump no está instalado"
command -v pg_restore >/dev/null || die "pg_restore no está instalado"
[[ -f "$DUMP_FILE" ]] || die "No se encontró el dump: $DUMP_FILE"

log "Verificando que la migración no se haya corrido ya en $DBNAME..."
ya_migrado=$("${PSQL_TARGET[@]}" -tAc "SELECT 1 FROM information_schema.schemata WHERE schema_name='catastro'")
if [[ "$ya_migrado" == "1" ]]; then
  die "El schema 'catastro' ya existe en $DBNAME. Esta migración ya se corrió antes; abortando para no duplicar datos."
fi

log "Verificando disponibilidad de la extensión postgis en el servidor..."
postgis_disponible=$("${PSQL_TARGET[@]}" -tAc "SELECT 1 FROM pg_available_extensions WHERE name='postgis'")
if [[ "$postgis_disponible" != "1" ]]; then
  die "La extensión postgis no está disponible en este servidor Postgres (instalá el paquete del sistema, ej. postgresql-<version>-postgis-3, antes de continuar; este script no instala paquetes del SO)."
fi

# postgis NO es relocatable (ALTER EXTENSION ... SET SCHEMA falla), y el dump
# filtrado (paso 4) referencia los tipos/funciones espaciales como
# "catastro.geometry", "catastro.st_astext", etc. porque en la base scratch la
# extensión termina viviendo en el schema que se renombra a catastro (paso 1 +
# paso 3). Si en destino postgis YA está instalada en otro schema (ej.
# "public" — es el caso real de polizador: carga_obra.obra_georeferencia ya es
# un PointField de GeoDjango, así que postgis casi seguro ya vive en "public"
# de antes), NO la reubicamos (DROP EXTENSION ... CASCADE se llevaría puesta
# esa columna existente). En cambio: GIS_SCHEMA apunta a donde YA vive postgis
# en destino, el paso 6 se salta la creación de la extensión, y el paso 4b
# reescribe el dump filtrado cambiando "catastro.<objeto-de-postgis>" por
# "$GIS_SCHEMA.<objeto-de-postgis>" antes de restaurar (paso 7).
log "Verificando dónde vive postgis (si es que ya está instalada) en $DBNAME..."
postgis_schema_actual=$("${PSQL_TARGET[@]}" -tAc "SELECT n.nspname FROM pg_extension e JOIN pg_namespace n ON n.oid = e.extnamespace WHERE e.extname = 'postgis'")
if [[ -z "$postgis_schema_actual" || "$postgis_schema_actual" == "catastro" ]]; then
  GIS_SCHEMA="catastro"
  NEEDS_GIS_REWRITE=0
  log "postgis no está instalada todavía (o ya está en catastro de una corrida anterior); se creará en catastro (paso 6)."
else
  GIS_SCHEMA="$postgis_schema_actual"
  NEEDS_GIS_REWRITE=1
  log "postgis ya está instalada en el schema '$GIS_SCHEMA' de $DBNAME (ej. por carga_obra.obra_georeferencia). No se reubica: se deja ahí, se salta el paso 6, y el dump filtrado se reescribe (paso 4b) para apuntar los objetos espaciales a '$GIS_SCHEMA' en vez de 'catastro'."
fi

# --- Paso 0: backup completo de la base de destino ---
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/${DBNAME}_pre_gdu_$(date +%Y%m%d_%H%M%S).dump"
log "Backup de seguridad de $DBNAME -> $BACKUP_FILE"
pg_dump -U "$DBUSER" -h "$DBHOST" -d "$DBNAME" -Fc -f "$BACKUP_FILE"
log "Backup completo ($(du -h "$BACKUP_FILE" | cut -f1))"

# --- Paso 1: base scratch con las extensiones ---
log "Creando base scratch $SCRATCH_DB..."
"${PSQL[@]}" -d postgres -c "DROP DATABASE IF EXISTS $SCRATCH_DB;"
"${PSQL[@]}" -d postgres -c "CREATE DATABASE $SCRATCH_DB OWNER $DBUSER;"

log "Creando extensiones postgis/pgcrypto en $SCRATCH_DB (requiere superusuario)..."
if ! sudo -n -u postgres psql -d "$SCRATCH_DB" -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS pgcrypto;" 2>/dev/null; then
  cat <<EOF

No se pudo crear la extensión automáticamente (se necesita sudo -u postgres sin
contraseña). Corré manualmente y volvé a ejecutar este script (es seguro
re-ejecutar desde el principio, $SCRATCH_DB se recrea):

  sudo -u postgres psql -d $SCRATCH_DB -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS pgcrypto;"

EOF
  die "Extensión postgis/pgcrypto no creada en $SCRATCH_DB"
fi

# --- Paso 2: restaurar el dump completo en la base scratch ---
RESTORE_LOG="/tmp/gdu_restore_scratch_$(date +%Y%m%d_%H%M%S).log"
log "Restaurando $DUMP_FILE en $SCRATCH_DB (los errores de ALTER...OWNER a roles inexistentes y de postgis-raster son esperables, ver notas de la migración)..."
"${PSQL[@]}" -d "$SCRATCH_DB" -f "$DUMP_FILE" > "$RESTORE_LOG" 2>&1 || true
log "Restore de $SCRATCH_DB terminado, log completo en $RESTORE_LOG"

# --- Paso 3: renombrar public -> catastro, descartar bookkeeping de Hasura ---
log "Renombrando schema public -> catastro y eliminando hdb_catalog/hdb_views..."
"${PSQL[@]}" -d "$SCRATCH_DB" -c "ALTER SCHEMA public RENAME TO catastro;"
"${PSQL[@]}" -d "$SCRATCH_DB" -c "DROP SCHEMA IF EXISTS hdb_catalog CASCADE; DROP SCHEMA IF EXISTS hdb_views CASCADE;"

# --- Paso 4: dump filtrado de los schemas GDU (pg_dump excluye automáticamente
# los objetos de la extensión postgis al filtrar por schema) ---
FILTERED_DUMP="/tmp/gdu_filtered_$(date +%Y%m%d_%H%M%S).dump"
log "Generando dump filtrado de ${SCHEMAS_GDU[*]} -> $FILTERED_DUMP"
SCHEMA_ARGS=()
for s in "${SCHEMAS_GDU[@]}"; do SCHEMA_ARGS+=(--schema="$s"); done
pg_dump -U "$DBUSER" -h "$DBHOST" -d "$SCRATCH_DB" "${SCHEMA_ARGS[@]}" --no-owner --no-privileges -Fc -f "$FILTERED_DUMP"

# --- Paso 4b: si postgis ya vivía en otro schema en destino (GIS_SCHEMA !=
# catastro), reescribir en el dump filtrado las referencias a los objetos de
# postgis (tipos, funciones, clases/familias de operadores) de "catastro.X" a
# "$GIS_SCHEMA.X". El dump -Fc de arriba es binario y no se puede editar, así
# que se convierte a texto plano y se restaura después con psql en vez de
# pg_restore (paso 7).
FILTERED_SQL=""
if [[ "$NEEDS_GIS_REWRITE" == "1" ]]; then
  log "Reescribiendo referencias a postgis de catastro.* -> ${GIS_SCHEMA}.* en el dump filtrado..."
  FILTERED_SQL="/tmp/gdu_filtered_rewritten_$(date +%Y%m%d_%H%M%S).sql"
  pg_restore --no-owner --no-privileges -f "$FILTERED_SQL" "$FILTERED_DUMP"

  GIS_OBJECTS=$("${PSQL[@]}" -d "$SCRATCH_DB" -tAc "
    SELECT DISTINCT format('%I.%I', n.nspname, o.name)
    FROM (
      SELECT typname AS name, typnamespace AS nsp, oid FROM pg_type
      UNION ALL
      SELECT proname, pronamespace, oid FROM pg_proc
      UNION ALL
      SELECT opcname, opcnamespace, oid FROM pg_opclass
      UNION ALL
      SELECT opfname, opfnamespace, oid FROM pg_opfamily
    ) o
    JOIN pg_namespace n ON n.oid = o.nsp AND n.nspname = 'catastro'
    JOIN pg_depend d ON d.objid = o.oid AND d.deptype = 'e'
    JOIN pg_extension e ON e.oid = d.refobjid AND e.extname = 'postgis'
  ")
  [[ -n "$GIS_OBJECTS" ]] || die "No se encontró ningún objeto de postgis en catastro de $SCRATCH_DB; no se puede reescribir el dump filtrado (¿falló el paso 1/3?)."

  SED_SCRIPT="/tmp/gdu_gis_rewrite_$(date +%Y%m%d_%H%M%S).sed"
  : > "$SED_SCRIPT"
  while IFS= read -r qualified; do
    name="${qualified#catastro.}"
    echo "s/\bcatastro\.${name}\b/${GIS_SCHEMA}.${name}/g" >> "$SED_SCRIPT"
  done <<< "$GIS_OBJECTS"
  log "$(wc -l < "$SED_SCRIPT") patrones de reescritura (tipos/funciones/opclasses de postgis) generados en $SED_SCRIPT"
  sed -i -f "$SED_SCRIPT" "$FILTERED_SQL"

  restantes=$(grep -c 'catastro\.\(geometry\|geography\|box2d\|box3d\|spheroid\|gidx\)\b' "$FILTERED_SQL" || true)
  if [[ "$restantes" != "0" ]]; then
    die "Quedaron $restantes referencias a catastro.<tipo espacial> sin reescribir en $FILTERED_SQL; revisá manualmente antes de continuar (no restaures a ciegas, se pierden datos espaciales en silencio)."
  fi
fi

# --- Paso 5: crear los schemas vacíos en destino (antes de la extensión, para
# que 'catastro' ya exista cuando se cree la extensión ahí adentro) ---
SCHEMA_LIST="/tmp/gdu_schemas_only_$(date +%Y%m%d_%H%M%S).list"
pg_restore -l "$FILTERED_DUMP" | grep "SCHEMA - " > "$SCHEMA_LIST"
log "Creando schemas vacíos en $DBNAME..."
pg_restore -U "$DBUSER" -h "$DBHOST" -d "$DBNAME" --no-owner --no-privileges -L "$SCHEMA_LIST" "$FILTERED_DUMP"

# --- Paso 6: extensión postgis en destino (superusuario) ---
if [[ "$GIS_SCHEMA" == "catastro" ]]; then
  log "Creando extensión postgis dentro de catastro en $DBNAME (requiere superusuario)..."
  if ! sudo -n -u postgres psql -v ON_ERROR_STOP=1 -d "$DBNAME" -c "CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA catastro; CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;" 2>/dev/null; then
    cat <<EOF

Corré manualmente y volvé a ejecutar este script (los schemas vacíos ya están
creados en $DBNAME, es seguro re-ejecutar desde acá — ver comentario "REANUDAR"
más abajo):

  sudo -u postgres psql -d $DBNAME -c "CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA catastro; CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;"

EOF
    die "Extensión postgis no creada en catastro de $DBNAME"
  fi
else
  log "postgis ya está instalada en '$GIS_SCHEMA' de $DBNAME (no se crea una extensión nueva; las referencias ya se reescribieron en el paso 4b). Solo se asegura pgcrypto."
  if ! sudo -n -u postgres psql -v ON_ERROR_STOP=1 -d "$DBNAME" -c "CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;" 2>/dev/null; then
    die "No se pudo asegurar la extensión pgcrypto en $DBNAME. Corré manualmente y reintentá: sudo -u postgres psql -d $DBNAME -c \"CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;\""
  fi
fi

# Chequeo de cordura: "CREATE EXTENSION IF NOT EXISTS" no falla (ni cambia de
# schema) si la extensión ya existía en otro lado — sin este chequeo el script
# seguiría de largo y el paso 7 perdería en silencio todas las tablas/vistas
# espaciales (ver chequeo equivalente más arriba, antes del backup).
postgis_schema_post=$("${PSQL_TARGET[@]}" -tAc "SELECT n.nspname FROM pg_extension e JOIN pg_namespace n ON n.oid = e.extnamespace WHERE e.extname = 'postgis'")
if [[ "$postgis_schema_post" != "$GIS_SCHEMA" ]]; then
  die "postgis quedó en el schema '$postgis_schema_post' en vez de '$GIS_SCHEMA' en $DBNAME. El restore del paso 7 fallaría en silencio para todas las tablas/vistas espaciales; abortando antes de continuar."
fi

# REANUDAR: si el script se cortó acá por el paso anterior, después de correr el
# comando manual de sudo podés saltar directo a pg_restore con el mismo
# $FILTERED_DUMP (quedó en /tmp) en vez de correr todo el script de nuevo.

# --- Paso 7: restaurar tablas/datos/vistas/funciones ---
DATA_RESTORE_LOG="/tmp/gdu_restore_destino_$(date +%Y%m%d_%H%M%S).log"
log "Restaurando datos en $DBNAME (los errores de 'schema already exists' y de 'spatial_ref_sys' son esperables; log completo en $DATA_RESTORE_LOG)..."
if [[ "$NEEDS_GIS_REWRITE" == "1" ]]; then
  "${PSQL_TARGET[@]}" -f "$FILTERED_SQL" > "$DATA_RESTORE_LOG" 2>&1 || true
else
  pg_restore -U "$DBUSER" -h "$DBHOST" -d "$DBNAME" --no-owner --no-privileges "$FILTERED_DUMP" > "$DATA_RESTORE_LOG" 2>&1 || true
fi

# --- Paso 8: search_path del rol para esta base ---
log "Configurando search_path del rol $DBUSER en $DBNAME..."
SEARCH_PATH="public, catastro, our, visualizador, vistas, audit"
if [[ "$GIS_SCHEMA" != "public" && "$GIS_SCHEMA" != "catastro" ]]; then
  SEARCH_PATH="$SEARCH_PATH, $GIS_SCHEMA"
fi
"${PSQL_TARGET[@]}" -c "ALTER ROLE $DBUSER IN DATABASE $DBNAME SET search_path = $SEARCH_PATH;"

# --- Paso 9: verificación de conteos ---
log "Verificando conteos de filas..."
"${PSQL_TARGET[@]}" -c "
SELECT 'catastro.uf' AS tabla, count(*) FROM catastro.uf
UNION ALL SELECT 'catastro.parcela', count(*) FROM catastro.parcela
UNION ALL SELECT 'catastro.catastrourbano', count(*) FROM catastro.catastrourbano
UNION ALL SELECT 'catastro.adjudicatario3450', count(*) FROM catastro.adjudicatario3450
UNION ALL SELECT 'our.vivienda', count(*) FROM our.vivienda
UNION ALL SELECT 'our.respuesta_encuesta', count(*) FROM our.respuesta_encuesta
UNION ALL SELECT 'visualizador.user', count(*) FROM visualizador.\"user\"
UNION ALL SELECT 'audit.audit_logs', count(*) FROM audit.audit_logs;
"

# --- Paso 10: limpieza ---
log "Eliminando base scratch $SCRATCH_DB..."
"${PSQL[@]}" -d postgres -c "DROP DATABASE IF EXISTS $SCRATCH_DB;"

log "Migración de datos completa. Backup previo en: $BACKUP_FILE"
log "Falta correr, desde el checkout de polizador en este servidor:"
log "  python manage.py migrate gdu"
log "  python manage.py migrar_usuarios_gdu"
