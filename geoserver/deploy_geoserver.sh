#!/usr/bin/env bash
#
# Automatiza el despliegue de GeoServer para WFS-T/GDU: levanta el contenedor
# Docker, publica el workspace/datastore/capas piloto (GS_FEATURETYPES, por
# default gdu:localidad + manzana/calle/vivienda_punto) vía REST, y configura
# el subsistema de seguridad (servicio de roles JDBC respaldado
# por Django, reglas de Data Access) escribiendo directamente los archivos del
# data dir -- porque la API REST de GeoServer no cubre servicios de roles ni
# reglas de acceso a datos, solo workspaces/datastores/capas.
#
# Reproduce exactamente lo que se validó a mano en el piloto local (ver
# /home/willy/.claude/plans/wfs-t-geoserver-qgis-gdu.md, Fase 1 y 2): el mismo
# contrato SQL para el servicio de roles JDBC, el mismo bridge admin->ADMIN
# (sin el cual activar este servicio de roles deja sin acceso al admin de
# GeoServer), y las mismas Data Access Rules probadas con anónimo/viewer/admin.
#
# Este script asume GeoServer y Postgres corriendo en servidores DISTINTOS
# (por eso las fases de Postgres se conectan siempre por TCP con usuario y
# contraseña -- nunca asume `sudo -u postgres` local como sí hace
# migrar_gdu_a_produccion.sh). Se puede correr la fase "postgres" desde
# cualquier máquina con acceso de red a la base, y la fase "geoserver" desde
# el servidor que va a correr el contenedor.
#
# Cambio deliberado respecto al piloto: la política global de encriptación de
# contraseñas de configuración pasa de "Weak PBE" (atada a la master key de
# ESE proceso de GeoServer, no portable) a texto plano
# (configPasswordEncrypterName=plainTextPasswordEncoder). Es lo que permite
# templatizar el config.xml del servicio de roles con una contraseña real y
# que funcione igual en cualquier servidor nuevo, sin pasos manuales por la
# UI para generar el cifrado. Restringí el acceso al filesystem del data dir
# en consecuencia (ver README.md).
#
# Uso:
#   ./deploy_geoserver.sh postgres   # crea roles + schema geoserver_auth en Postgres
#   ./deploy_geoserver.sh geoserver  # levanta/actualiza el contenedor GeoServer
#   ./deploy_geoserver.sh verify     # corre la misma batería de pruebas allow/deny de la Fase 2
#   ./deploy_geoserver.sh all        # las tres fases en orden
#
# Variables de entorno requeridas -- ver README.md para la lista completa y
# ejemplos. Ninguna tiene default porque son todas específicas del servidor
# de destino (todavía no definido) o son secretos.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/templates"
SQL_DIR="$SCRIPT_DIR/sql"
PLUGIN_DIR="$SCRIPT_DIR/plugin"
RENDERED_DIR="$SCRIPT_DIR/.rendered"

# Si existe geoserver/.env, se carga antes que nada (mismo patrón que
# polizador/.env, pero acá no hay django-environ leyéndolo por nosotros --
# hay que sourcearlo a mano). No versionado (ver .gitignore): son secretos y
# valores específicos de un servidor de destino puntual. Formato simple
# VAR=valor por línea (sin "export", aunque tampoco molesta si lo tiene); lo
# que defina este archivo pisa cualquier valor ya exportado en el shell para
# esa misma variable, como con cualquier `source`.
if [[ -f "$SCRIPT_DIR/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/.env"
  set +a
fi

log() { echo -e "\n>>> $*"; }
die() { echo "ERROR: $*" >&2; exit 1; }
require_env() { local var="$1"; [[ -n "${!var:-}" ]] || die "Falta la variable de entorno $var"; }

# --- Configuración (con default) ---
GEOSERVER_CONTAINER_NAME="${GEOSERVER_CONTAINER_NAME:-geoserver-gdu}"
GEOSERVER_IMAGE="${GEOSERVER_IMAGE:-docker.osgeo.org/geoserver:2.26.2}"
GEOSERVER_HTTP_PORT="${GEOSERVER_HTTP_PORT:-8080}"
GEOSERVER_DATA_DIR_HOST="${GEOSERVER_DATA_DIR_HOST:-/opt/geoserver_data}"
GEOSERVER_ADMIN_USER="${GEOSERVER_ADMIN_USER:-admin}"
GEOSERVER_URL="${GEOSERVER_URL:-http://127.0.0.1:${GEOSERVER_HTTP_PORT}/geoserver}"
PGPORT="${PGPORT:-5432}"

# Identificadores del workspace/datastore/capa piloto. Quedan como variables
# (no hardcodeados en el cuerpo del script) para que sumar capas en la Fase 4
# sea extender esta sección, no reescribir la lógica de provisioning.
GS_WORKSPACE="${GS_WORKSPACE:-gdu}"
GS_DATASTORE="${GS_DATASTORE:-catastro}"
GS_NAMESPACE_URI="${GS_NAMESPACE_URI:-http://gdu}"
GS_PG_SCHEMA="${GS_PG_SCHEMA:-catastro}"
# Lista separada por espacios. El primero (GS_FEATURETYPE_DEEP_TEST) es sobre
# el que corre el chequeo profundo de phase_verify (insert+update+delete con
# geometría) -- las demás capas solo reciben el chequeo liviano (oculta para
# anónimo + un Update de atributo no geométrico). Sumar una capa nueva es
# agregarla acá + su GRANT en sql/02_provision_schema.sql + sus reglas en
# templates/layers.properties.
#
# Spike N:N (ver plan en-lugar-de-geoserver-hashed-cupcake.md): intervencion/
# inspector/ejecutor/intervencion_inspector/intervencion_ejecutor son tablas
# de soporte del formulario N:N de "Intervención" (forms/nn.py), sin geometría
# propia y sin rol Django dedicado todavía -- gate provisional GDU_ADMIN_USER
# para lectura y escritura en templates/layers.properties (el wildcard
# *.*.r=* de ese archivo es lectura PÚBLICA, no alcanza dejarlas sin regla).
GS_FEATURETYPES="${GS_FEATURETYPES:-localidad manzana calle vivienda_punto intervencion inspector ejecutor intervencion_inspector intervencion_ejecutor plano_mensura plano_mensura_intervencion tierra plano_mensura_tierra}"
GS_FEATURETYPE_DEEP_TEST="${GS_FEATURETYPE_DEEP_TEST:-localidad}"
GS_FEATURETYPE_SRS="${GS_FEATURETYPE_SRS:-EPSG:22175}"
# Tablas de GS_FEATURETYPES sin columna updated_by/updated_at (tablas
# intermedias N:N puras, ej. intervencion_inspector: solo 2 FKs + id) -- para
# estas, phase_verify salta la aserción de updated_by en el chequeo liviano
# (no aplica) y se queda solo con "oculta para anónimo".
GS_FEATURETYPES_NO_AUDIT="${GS_FEATURETYPES_NO_AUDIT:-intervencion_inspector plano_mensura_intervencion plano_mensura_tierra}"

# LDAP (autenticación -- NO autorización, eso lo sigue resolviendo el servicio
# de roles JDBC por username, sin cambios). Opcional: si no se define
# LDAP_BIND_DN/LDAP_BIND_PASSWORD, overlay_security_config no toca nada de
# LDAP y el proveedor sigue siendo solo 'default'. Los valores de conexión
# (server/filtro/atributo) son los mismos que ya usa Django
# (polizador/.env: GDU_LDAP_*) -- tienen default porque son infraestructura
# fija de IPDUV, no un secreto; el bind DN y su contraseña si son requeridos
# explícitamente, sin default, para no asumir por accidente una cuenta de
# producción en un deploy a otro entorno.
LDAP_PROVIDER_NAME="${LDAP_PROVIDER_NAME:-ldap-ipduv}"
LDAP_SERVER_URL="${LDAP_SERVER_URL:-ldap://10.106.16.3:389/dc=ipduv,dc=gov,dc=ar}"
# OJO: el default de LDAP_USER_FILTER NO se puede escribir como
# ${LDAP_USER_FILTER:-(sAMAccountName={0})} -- las llaves de "{0}" dentro del
# valor default confunden el parser de bash al buscar el cierre de ${...} y
# terminan reordenando caracteres (se reprodujo aislado: da
# "(sAMAccountName={0)}", con el ")" y el "}" invertidos). Asignación
# explícita en dos pasos para no depender de ese parseo.
LDAP_USER_FILTER="${LDAP_USER_FILTER:-}"
[[ -z "$LDAP_USER_FILTER" ]] && LDAP_USER_FILTER='(sAMAccountName={0})'
LDAP_USER_NAME_ATTRIBUTE="${LDAP_USER_NAME_ATTRIBUTE:-sAMAccountName}"

mkdir -p "$RENDERED_DIR"

# Reemplaza tokens __NOMBRE__ por el valor de la variable de entorno NOMBRE.
# No usa envsubst para no agregar una dependencia nueva al repo.
render_template() {
  local src="$1" dest="$2"; shift 2
  local content; content="$(cat "$src")"
  for var in "$@"; do
    local token="__${var}__"
    content="${content//$token/${!var}}"
  done
  printf '%s' "$content" > "$dest"
}

wait_for_geoserver() {
  local timeout="${1:-90}" waited=0
  log "Esperando a que GeoServer responda en $GEOSERVER_URL ..."
  until curl -sf -o /dev/null "$GEOSERVER_URL/web/" 2>/dev/null; do
    sleep 2; waited=$((waited + 2))
    [[ $waited -lt $timeout ]] || die "GeoServer no respondió después de ${timeout}s"
  done
  log "GeoServer respondiendo (${waited}s)"
}

REST_BODY_FILE="$RENDERED_DIR/.rest_body"

rest() {
  # rest <método> <path> [archivo-json] -- devuelve SOLO el código HTTP por
  # stdout; el cuerpo de la respuesta queda en $REST_BODY_FILE (leerlo con
  # "cat $REST_BODY_FILE" si hace falta). Nunca mezcla cuerpo y código en el
  # mismo stream a propósito: un primer intento concatenaba el código
  # después del cuerpo ("cat archivo; echo \"\$code\"") y lo separaba de
  # nuevo por líneas/bytes en el caller -- se rompió en el primer uso real
  # contra el piloto (el chequeo de "¿ya existe el datastore?" daba siempre
  # falso) porque el cuerpo JSON de GeoServer no termina en salto de línea:
  # el código quedaba pegado directo al final del cuerpo, sin separador
  # confiable para partirlo de nuevo. Separar los dos streams desde el
  # origen (uno a archivo, el otro a stdout) evita la ambigüedad de raíz.
  local method="$1" path="$2" body="${3:-}"
  local args=(-s -o "$REST_BODY_FILE" -w '%{http_code}' -u "${GEOSERVER_ADMIN_USER}:${GEOSERVER_ADMIN_PASSWORD}" -X "$method")
  [[ -n "$body" ]] && args+=(-H "Content-Type: application/json" --data-binary "@$body")
  curl "${args[@]}" "${GEOSERVER_URL}${path}"
}

rest_check() {
  # Como rest(), pero aborta si el código HTTP no es 2xx -- para llamadas de
  # creación/actualización donde antes se descartaba la respuesta entera con
  # ">/dev/null" y un error quedaba completamente silencioso.
  local code; code="$(rest "$@")"
  case "$code" in
    2??) ;;
    *) die "REST $1 $2 -> HTTP $code: $(cat "$REST_BODY_FILE" 2>/dev/null)" ;;
  esac
}

anon_oculta() {
  # anon_oculta <typename> -- true si un GetFeature anónimo NO puede leer
  # esa capa. Con mode=CHALLENGE (ver templates/layers.properties) la
  # denegación puede llegar de DOS formas distintas según en qué punto del
  # pipeline la corte Spring Security: un ExceptionReport de GeoServer
  # (cuerpo con "unknown"/"Exception", típico tras un /rest/reload en
  # caliente) o directo una página de error 401 de Tomcat sin ese texto
  # (típico después de un restart completo del contenedor, visto en vivo al
  # generalizar a plano_mensura/tierra) -- se acepta cualquiera de las dos
  # en vez de depender de un único formato de respuesta.
  local typename="$1" code body
  code="$(curl -s -o "$REST_BODY_FILE" -w '%{http_code}' "${GEOSERVER_URL}/${GS_WORKSPACE}/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=${typename}&count=1")"
  body="$(cat "$REST_BODY_FILE" 2>/dev/null)"
  [[ "$code" == "401" || "$code" == "403" || "$body" == *"unknown"* || "$body" == *"Exception"* ]]
}

phase_postgres() {
  log "Fase Postgres: creando roles (necesita superusuario) y schema geoserver_auth"
  require_env PGHOST
  require_env PGDATABASE
  require_env PG_SUPERUSER
  require_env PG_SUPERUSER_PASSWORD
  require_env PG_APP_USER
  require_env PG_APP_PASSWORD
  require_env GEOSERVER_DS_PASSWORD
  require_env GEOSERVER_SECURITY_DB_PASSWORD

  render_template "$SQL_DIR/01_provision_roles.sql.tmpl" "$RENDERED_DIR/01_provision_roles.sql" \
    GEOSERVER_DS_PASSWORD GEOSERVER_SECURITY_DB_PASSWORD

  log "Aplicando 01_provision_roles.sql como $PG_SUPERUSER (CREATE ROLE)..."
  PGPASSWORD="$PG_SUPERUSER_PASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PG_SUPERUSER" -d "$PGDATABASE" \
    -v ON_ERROR_STOP=1 -f "$RENDERED_DIR/01_provision_roles.sql"

  log "Aplicando 02_provision_schema.sql como $PG_APP_USER (schema geoserver_auth + grants)..."
  PGPASSWORD="$PG_APP_PASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PG_APP_USER" -d "$PGDATABASE" \
    -v ON_ERROR_STOP=1 -f "$SQL_DIR/02_provision_schema.sql"

  log "Fase Postgres OK"
}

overlay_security_config() {
  log "Escribiendo configuración de seguridad en el data dir del contenedor..."
  require_env PGHOST
  require_env PGDATABASE
  require_env GEOSERVER_SECURITY_DB_PASSWORD

  render_template "$TEMPLATES_DIR/role-service-config.xml.tmpl" "$RENDERED_DIR/role-service-config.xml" \
    PGHOST PGPORT PGDATABASE GEOSERVER_SECURITY_DB_PASSWORD

  docker exec "$GEOSERVER_CONTAINER_NAME" mkdir -p /opt/geoserver_data/security/role/django
  docker cp "$RENDERED_DIR/role-service-config.xml" "$GEOSERVER_CONTAINER_NAME:/opt/geoserver_data/security/role/django/config.xml"
  docker cp "$TEMPLATES_DIR/rolesddl.xml" "$GEOSERVER_CONTAINER_NAME:/opt/geoserver_data/security/role/django/rolesddl.xml"
  docker cp "$TEMPLATES_DIR/roles-django.dml.xml" "$GEOSERVER_CONTAINER_NAME:/opt/geoserver_data/security/role/django/roles-django.dml.xml"
  docker cp "$TEMPLATES_DIR/layers.properties" "$GEOSERVER_CONTAINER_NAME:/opt/geoserver_data/security/layers.properties"

  # OJO: a diferencia de todo lo anterior en esta función, este jar NO va al
  # data dir persistente (/opt/geoserver_data), va al WEB-INF/lib del webapp
  # -- por eso se copia acá en cada corrida (idempotente, se sobreescribe) en
  # vez de una sola vez: si el contenedor se recrea desde la imagen stock,
  # WEB-INF/lib vuelve a como venía de fábrica y no incluye este plugin.
  log "Instalando plugin gdu-updated-by-listener.jar (updated_by por usuario autenticado)..."
  docker cp "$PLUGIN_DIR/gdu-updated-by-listener.jar" "$GEOSERVER_CONTAINER_NAME:/usr/local/tomcat/webapps/geoserver/WEB-INF/lib/gdu-updated-by-listener.jar"

  if [[ -n "${LDAP_BIND_DN:-}" && -n "${LDAP_BIND_PASSWORD:-}" ]]; then
    log "Configurando proveedor de autenticación LDAP ($LDAP_PROVIDER_NAME)..."
    render_template "$TEMPLATES_DIR/ldap-auth-config.xml.tmpl" "$RENDERED_DIR/ldap-auth-config.xml" \
      LDAP_PROVIDER_NAME LDAP_SERVER_URL LDAP_USER_FILTER LDAP_USER_NAME_ATTRIBUTE LDAP_BIND_DN LDAP_BIND_PASSWORD
    docker exec "$GEOSERVER_CONTAINER_NAME" mkdir -p "/opt/geoserver_data/security/auth/${LDAP_PROVIDER_NAME}"
    docker cp "$RENDERED_DIR/ldap-auth-config.xml" "$GEOSERVER_CONTAINER_NAME:/opt/geoserver_data/security/auth/${LDAP_PROVIDER_NAME}/config.xml"
    EXTRA_AUTH_PROVIDERS="<string>${LDAP_PROVIDER_NAME}</string>"
  else
    log "LDAP_BIND_DN/LDAP_BIND_PASSWORD no definidos -- se omite el proveedor LDAP, queda solo 'default' (admin local)"
    EXTRA_AUTH_PROVIDERS=""
  fi
  render_template "$TEMPLATES_DIR/security-config.xml.tmpl" "$RENDERED_DIR/security-config.xml" EXTRA_AUTH_PROVIDERS
  docker cp "$RENDERED_DIR/security-config.xml" "$GEOSERVER_CONTAINER_NAME:/opt/geoserver_data/security/config.xml"

  log "Reiniciando el contenedor para que tome la config de seguridad (un simple /rest/reload no alcanza para el servicio de roles JDBC ni para un proveedor de autenticación nuevo -- confirmado a mano en el piloto)..."
  docker restart "$GEOSERVER_CONTAINER_NAME" >/dev/null
  wait_for_geoserver
}

rest_provision() {
  log "Publicando workspace/datastore/capa vía REST (idempotente)..."
  require_env GEOSERVER_ADMIN_PASSWORD
  require_env PGHOST
  require_env PGDATABASE
  require_env GEOSERVER_DS_PASSWORD

  local code
  code="$(rest GET "/rest/workspaces/${GS_WORKSPACE}.json")"
  if [[ "$code" != "200" ]]; then
    log "Creando workspace $GS_WORKSPACE"
    printf '{"workspace":{"name":"%s"}}' "$GS_WORKSPACE" > "$RENDERED_DIR/workspace.json"
    rest_check POST "/rest/workspaces" "$RENDERED_DIR/workspace.json"
  else
    log "Workspace $GS_WORKSPACE ya existe, no se toca"
  fi

  code="$(rest GET "/rest/workspaces/${GS_WORKSPACE}/datastores/${GS_DATASTORE}.json")"
  cat > "$RENDERED_DIR/datastore.json" <<JSON
{
  "dataStore": {
    "name": "${GS_DATASTORE}",
    "connectionParameters": {
      "entry": [
        {"@key": "dbtype", "\$": "postgis"},
        {"@key": "host", "\$": "${PGHOST}"},
        {"@key": "port", "\$": "${PGPORT}"},
        {"@key": "database", "\$": "${PGDATABASE}"},
        {"@key": "schema", "\$": "${GS_PG_SCHEMA}"},
        {"@key": "user", "\$": "geoserver_piloto"},
        {"@key": "passwd", "\$": "${GEOSERVER_DS_PASSWORD}"},
        {"@key": "namespace", "\$": "${GS_NAMESPACE_URI}"},
        {"@key": "Expose primary keys", "\$": "true"}
      ]
    }
  }
}
JSON
  if [[ "$code" != "200" ]]; then
    log "Creando datastore $GS_DATASTORE"
    rest_check POST "/rest/workspaces/${GS_WORKSPACE}/datastores" "$RENDERED_DIR/datastore.json"
  else
    log "Datastore $GS_DATASTORE ya existe, actualizando parámetros de conexión"
    rest_check PUT "/rest/workspaces/${GS_WORKSPACE}/datastores/${GS_DATASTORE}" "$RENDERED_DIR/datastore.json"
  fi

  local ft
  for ft in $GS_FEATURETYPES; do
    code="$(rest GET "/rest/workspaces/${GS_WORKSPACE}/datastores/${GS_DATASTORE}/featuretypes/${ft}.json")"
    if [[ "$code" != "200" ]]; then
      log "Publicando capa $GS_WORKSPACE:$ft"
      cat > "$RENDERED_DIR/featuretype-${ft}.json" <<JSON
{
  "featureType": {
    "name": "${ft}",
    "nativeName": "${ft}",
    "title": "${ft^}",
    "srs": "${GS_FEATURETYPE_SRS}",
    "projectionPolicy": "FORCE_DECLARED",
    "enabled": true
  }
}
JSON
      rest_check POST "/rest/workspaces/${GS_WORKSPACE}/datastores/${GS_DATASTORE}/featuretypes" "$RENDERED_DIR/featuretype-${ft}.json"
    else
      log "Capa $GS_WORKSPACE:$ft ya publicada, no se toca"
    fi
  done
}

phase_geoserver() {
  require_env GEOSERVER_ADMIN_PASSWORD

  if docker inspect "$GEOSERVER_CONTAINER_NAME" >/dev/null 2>&1; then
    log "Contenedor $GEOSERVER_CONTAINER_NAME ya existe, asegurando que esté corriendo"
    docker start "$GEOSERVER_CONTAINER_NAME" >/dev/null 2>&1 || true
  else
    log "Creando contenedor $GEOSERVER_CONTAINER_NAME ($GEOSERVER_IMAGE)"
    mkdir -p "$GEOSERVER_DATA_DIR_HOST"
    docker run -d \
      --name "$GEOSERVER_CONTAINER_NAME" \
      --restart unless-stopped \
      -p "${GEOSERVER_HTTP_PORT}:8080" \
      -e GEOSERVER_ADMIN_USER="$GEOSERVER_ADMIN_USER" \
      -e GEOSERVER_ADMIN_PASSWORD="$GEOSERVER_ADMIN_PASSWORD" \
      -e SKIP_DEMO_DATA=true \
      -v "${GEOSERVER_DATA_DIR_HOST}:/opt/geoserver_data" \
      "$GEOSERVER_IMAGE" >/dev/null
  fi

  wait_for_geoserver 180
  overlay_security_config
  rest_provision
  log "Fase GeoServer OK"
}

phase_verify() {
  require_env GEOSERVER_ADMIN_PASSWORD
  log "Verificando acceso admin..."
  local admin_roles; admin_roles="$(curl -s -u "${GEOSERVER_ADMIN_USER}:${GEOSERVER_ADMIN_PASSWORD}" "${GEOSERVER_URL}/rest/security/roles/user/${GEOSERVER_ADMIN_USER}.json")"
  [[ "$admin_roles" == *ADMIN* ]] || die "El usuario $GEOSERVER_ADMIN_USER no resuelve a ADMIN vía el servicio de roles django -- revisar el bridge admin->ADMIN en geoserver_auth.user_roles antes de activar este servicio de roles en Settings."
  log "OK: $GEOSERVER_ADMIN_USER -> $admin_roles"

  log "Verificando lectura anónima de ${GS_WORKSPACE}:${GS_FEATURETYPE_DEEP_TEST} (debe estar oculta)..."
  anon_oculta "${GS_WORKSPACE}:${GS_FEATURETYPE_DEEP_TEST}" || die "Un usuario anónimo pudo leer ${GS_WORKSPACE}:${GS_FEATURETYPE_DEEP_TEST} -- revisar templates/layers.properties"
  log "OK: capa oculta para anónimo"

  log "Verificando escritura admin (WFS-T) en ${GS_FEATURETYPE_DEEP_TEST}..."
  local upd; upd="$(curl -s -u "${GEOSERVER_ADMIN_USER}:${GEOSERVER_ADMIN_PASSWORD}" -H "Content-Type: text/xml" --data-binary @- "${GEOSERVER_URL}/${GS_WORKSPACE}/wfs" <<XML
<?xml version="1.0" encoding="UTF-8"?>
<wfs:Transaction service="WFS" version="1.1.0" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gdu="${GS_NAMESPACE_URI}" xmlns:ogc="http://www.opengis.net/ogc">
  <wfs:Update typeName="${GS_WORKSPACE}:${GS_FEATURETYPE_DEEP_TEST}">
    <wfs:Property><wfs:Name>updated_by</wfs:Name><wfs:Value>deploy_verify</wfs:Value></wfs:Property>
    <ogc:Filter><ogc:PropertyIsEqualTo><ogc:PropertyName>id</ogc:PropertyName><ogc:Literal>1</ogc:Literal></ogc:PropertyIsEqualTo></ogc:Filter>
  </wfs:Update>
</wfs:Transaction>
XML
)"
  [[ "$upd" == *"totalUpdated>1"* ]] || die "La escritura de prueba como admin falló: $upd"
  log "OK: WFS-T Update como admin funciona"

  log "Verificando que el plugin gdu-updated-by-listener reemplace updated_by por el usuario autenticado real (mandamos 'deploy_verify' a propósito, tiene que quedar '${GEOSERVER_ADMIN_USER}')..."
  local feat; feat="$(curl -s -u "${GEOSERVER_ADMIN_USER}:${GEOSERVER_ADMIN_PASSWORD}" "${GEOSERVER_URL}/${GS_WORKSPACE}/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=${GS_WORKSPACE}:${GS_FEATURETYPE_DEEP_TEST}&featureID=${GS_FEATURETYPE_DEEP_TEST}.1")"
  [[ "$feat" == *"updated_by>${GEOSERVER_ADMIN_USER}<"* ]] || die "updated_by no quedó en '${GEOSERVER_ADMIN_USER}' -- ¿se copió gdu-updated-by-listener.jar a WEB-INF/lib? ¿corrió 02_provision_schema.sql (trigger con COALESCE)? Respuesta: $feat"
  log "OK: updated_by refleja al usuario autenticado, no lo que mandó el cliente"

  log "Chequeo liviano del resto de las capas (${GS_FEATURETYPES})..."
  local ft
  for ft in $GS_FEATURETYPES; do
    [[ "$ft" == "$GS_FEATURETYPE_DEEP_TEST" ]] && continue  # ya se probó arriba a fondo

    anon_oculta "${GS_WORKSPACE}:${ft}" || die "Un usuario anónimo pudo leer ${GS_WORKSPACE}:${ft} -- revisar templates/layers.properties"

    if [[ " $GS_FEATURETYPES_NO_AUDIT " == *" $ft "* ]]; then
      log "OK: $ft (oculta para anónimo -- sin updated_by, se salta el chequeo de Update; el guardado N:N real se valida a mano en QGIS)"
      continue
    fi

    # El id=1 no existe en todas las tablas (ej. intervencion_ejecutor: su
    # secuencia ya viene usada de antes, no tiene fila con id=1) -- se
    # resuelve un id real existente en vez de asumirlo, para no confundir
    # "no hay fila con ese id" (totalUpdated=0, no es un error de permisos)
    # con una falla real del mecanismo.
    local ft_probe ft_id
    ft_probe="$(curl -s -u "${GEOSERVER_ADMIN_USER}:${GEOSERVER_ADMIN_PASSWORD}" "${GEOSERVER_URL}/${GS_WORKSPACE}/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=${GS_WORKSPACE}:${ft}&count=1")"
    ft_id="$(echo "$ft_probe" | grep -o "gml:id=\"${ft}\.[0-9]\+\"" | head -1 | grep -o '[0-9]\+')"
    [[ -n "$ft_id" ]] || die "$ft: no se encontró ninguna fila para probar el Update (¿la tabla está vacía? sembrar al menos una fila de prueba, o agregar $ft a GS_FEATURETYPES_NO_AUDIT si no corresponde este chequeo)"

    curl -s -u "${GEOSERVER_ADMIN_USER}:${GEOSERVER_ADMIN_PASSWORD}" -H "Content-Type: text/xml" --data-binary @- "${GEOSERVER_URL}/${GS_WORKSPACE}/wfs" <<XML >/dev/null
<?xml version="1.0" encoding="UTF-8"?>
<wfs:Transaction service="WFS" version="1.1.0" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gdu="${GS_NAMESPACE_URI}" xmlns:ogc="http://www.opengis.net/ogc">
  <wfs:Update typeName="${GS_WORKSPACE}:${ft}">
    <wfs:Property><wfs:Name>updated_by</wfs:Name><wfs:Value>deploy_verify</wfs:Value></wfs:Property>
    <ogc:Filter><ogc:PropertyIsEqualTo><ogc:PropertyName>id</ogc:PropertyName><ogc:Literal>${ft_id}</ogc:Literal></ogc:PropertyIsEqualTo></ogc:Filter>
  </wfs:Update>
</wfs:Transaction>
XML
    local ft_feat; ft_feat="$(curl -s -u "${GEOSERVER_ADMIN_USER}:${GEOSERVER_ADMIN_PASSWORD}" "${GEOSERVER_URL}/${GS_WORKSPACE}/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=${GS_WORKSPACE}:${ft}&featureID=${ft}.${ft_id}")"
    [[ "$ft_feat" == *"updated_by>${GEOSERVER_ADMIN_USER}<"* ]] || die "$ft: updated_by no quedó en '${GEOSERVER_ADMIN_USER}' tras un Update de prueba -- revisar el GRANT en sql/02_provision_schema.sql y las reglas en templates/layers.properties"
    log "OK: $ft (oculta para anónimo, escritura admin funciona, updated_by correcto)"
  done

  if [[ -n "${LDAP_BIND_DN:-}" && -n "${LDAP_BIND_PASSWORD:-}" ]]; then
    log "Verificando el proveedor LDAP (bind real contra el AD, con la cuenta de bind)..."
    local ldap_user="${LDAP_BIND_DN##*\\}"  # 'IPDUV\admindeu' -> 'admindeu' (o tal cual si no tiene dominio)
    local code_ok code_bad
    code_ok="$(curl -s -o /dev/null -w '%{http_code}' -u "${ldap_user}:${LDAP_BIND_PASSWORD}" "${GEOSERVER_URL}/rest/about/version.json")"
    code_bad="$(curl -s -o /dev/null -w '%{http_code}' -u "${ldap_user}:contraseña-incorrecta-a-proposito" "${GEOSERVER_URL}/rest/about/version.json")"
    # 403 = autenticó bien pero sin roles (normal: la cuenta de bind no es un usuario de Django);
    # 401 = no autenticó. La distinción entre ambos solo es posible con un bind real contra el AD.
    [[ "$code_ok" == "403" || "$code_ok" == "200" ]] || die "LDAP: '$ldap_user' con la contraseña correcta dio HTTP $code_ok (se esperaba 200 o 403) -- revisar serverURL/userFilter/bind DN"
    [[ "$code_bad" == "401" ]] || die "LDAP: una contraseña incorrecta para '$ldap_user' dio HTTP $code_bad en vez de 401 -- ¿el bind no está validando contra el AD de verdad?"
    log "OK: LDAP autentica de verdad contra el AD (correcta -> $code_ok, incorrecta -> $code_bad)"
  else
    log "LDAP no configurado (LDAP_BIND_DN/LDAP_BIND_PASSWORD vacíos) -- se omite esa verificación"
  fi

  log "Verificación completa OK"
}

case "${1:-}" in
  postgres) phase_postgres ;;
  geoserver) phase_geoserver ;;
  verify) phase_verify ;;
  all) phase_postgres; phase_geoserver; phase_verify ;;
  *) die "Uso: $0 {postgres|geoserver|verify|all} -- ver README.md" ;;
esac
