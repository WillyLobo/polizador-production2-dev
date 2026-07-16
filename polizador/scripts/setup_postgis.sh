#!/usr/bin/env bash
# Verifica que la base de datos de Polizador tenga la extensión PostGIS
# instalada, y si no la tiene, indica (o ejecuta) el comando necesario.
#
# Uso:
#   ./scripts/setup_postgis.sh          # sólo verifica / muestra el comando
#   ./scripts/setup_postgis.sh --yes    # además intenta instalarla via sudo
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."   # polizador/, donde vive .env

ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "No se encontró $ENV_FILE en $(pwd)" >&2
    exit 1
fi

DBHOST=$(grep -m1 '^DBHOST=' "$ENV_FILE" | cut -d= -f2-)
DBUSER=$(grep -m1 '^DBUSER=' "$ENV_FILE" | cut -d= -f2-)
DBNAME=$(grep -m1 '^DBNAME=' "$ENV_FILE" | cut -d= -f2-)
DBPASSWORD=$(grep -m1 '^DBPASSWORD=' "$ENV_FILE" | cut -d= -f2-)

if ! command -v psql >/dev/null 2>&1; then
    echo "psql no está disponible en PATH." >&2
    exit 1
fi

echo "== Base de datos: $DBNAME@$DBHOST (usuario app: $DBUSER) =="

PG_VERSION_STR=$(PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -U "$DBUSER" -d "$DBNAME" -tAc "SHOW server_version;")
PG_MAJOR=$(echo "$PG_VERSION_STR" | grep -oE '^[0-9]+')
echo "PostgreSQL server version: $PG_VERSION_STR (major: $PG_MAJOR)"

INSTALLED=$(PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -U "$DBUSER" -d "$DBNAME" -tAc \
    "SELECT 1 FROM pg_extension WHERE extname='postgis';")

if [ "$INSTALLED" = "1" ]; then
    VERSION=$(PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -U "$DBUSER" -d "$DBNAME" -tAc \
        "SELECT extversion FROM pg_extension WHERE extname='postgis';")
    echo "OK: la extensión postgis ya está instalada en '$DBNAME' (versión $VERSION)."
    exit 0
fi

echo "La extensión postgis NO está instalada en '$DBNAME'."

AVAILABLE=$(PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -U "$DBUSER" -d "$DBNAME" -tAc \
    "SELECT 1 FROM pg_available_extensions WHERE name='postgis';")

if [ "$AVAILABLE" != "1" ]; then
    PKG="postgresql-${PG_MAJOR}-postgis-3"
    cat <<EOF

El paquete de PostGIS no está disponible para este servidor PostgreSQL.
Instalalo en el host de la base de datos ($DBHOST) con:

    sudo apt-get update && sudo apt-get install -y $PKG

Después volvé a correr este script.
EOF
    exit 1
fi

CREATE_CMD="sudo -u postgres psql -d \"$DBNAME\" -c \"CREATE EXTENSION IF NOT EXISTS postgis;\""

cat <<EOF

postgis está disponible para instalar. Se requiere un rol superusuario
de PostgreSQL (el usuario de la app, '$DBUSER', no tiene permiso).

Ejecutá lo siguiente en el host de la base de datos ($DBHOST):

    $CREATE_CMD

EOF

if [ "${1:-}" = "--yes" ]; then
    echo "Intentando ejecutarlo ahora vía sudo..."
    sudo -u postgres psql -d "$DBNAME" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
    echo "Listo. Verificando..."
    PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -U "$DBUSER" -d "$DBNAME" -tAc \
        "SELECT extname, extversion FROM pg_extension WHERE extname='postgis';"
fi
