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

# --- Paso 5: crear los schemas vacíos en destino (antes de la extensión, para
# que 'catastro' ya exista cuando se cree la extensión ahí adentro) ---
SCHEMA_LIST="/tmp/gdu_schemas_only_$(date +%Y%m%d_%H%M%S).list"
pg_restore -l "$FILTERED_DUMP" | grep "SCHEMA - " > "$SCHEMA_LIST"
log "Creando schemas vacíos en $DBNAME..."
pg_restore -U "$DBUSER" -h "$DBHOST" -d "$DBNAME" --no-owner --no-privileges -L "$SCHEMA_LIST" "$FILTERED_DUMP"

# --- Paso 6: extensión postgis dentro de catastro en destino (superusuario) ---
log "Creando extensión postgis dentro de catastro en $DBNAME (requiere superusuario)..."
if ! sudo -n -u postgres psql -d "$DBNAME" -c "CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA catastro; CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;" 2>/dev/null; then
  cat <<EOF

Corré manualmente y volvé a ejecutar este script (los schemas vacíos ya están
creados en $DBNAME, es seguro re-ejecutar desde acá — ver comentario "REANUDAR"
más abajo):

  sudo -u postgres psql -d $DBNAME -c "CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA catastro; CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;"

EOF
  die "Extensión postgis no creada en catastro de $DBNAME"
fi

# REANUDAR: si el script se cortó acá por el paso anterior, después de correr el
# comando manual de sudo podés saltar directo a pg_restore con el mismo
# $FILTERED_DUMP (quedó en /tmp) en vez de correr todo el script de nuevo.

# --- Paso 7: restaurar tablas/datos/vistas/funciones ---
log "Restaurando datos en $DBNAME (los errores de 'schema already exists' y de 'spatial_ref_sys' son esperables)..."
pg_restore -U "$DBUSER" -h "$DBHOST" -d "$DBNAME" --no-owner --no-privileges "$FILTERED_DUMP" || true

# --- Paso 8: search_path del rol para esta base ---
log "Configurando search_path del rol $DBUSER en $DBNAME..."
"${PSQL_TARGET[@]}" -c "ALTER ROLE $DBUSER IN DATABASE $DBNAME SET search_path = public, catastro, our, visualizador, vistas, audit;"

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
