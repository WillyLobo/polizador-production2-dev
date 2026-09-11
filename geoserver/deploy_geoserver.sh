#!/usr/bin/env bash
#
# Automatiza el despliegue de GeoServer para WFS-T/GDU: instala/actualiza
# GeoServer como servicio nativo (distribución "bin" standalone oficial,
# Jetty embebido, systemd -- sin Docker, sin Tomcat), publica
# el workspace/datastore/capas piloto (GS_FEATURETYPES, por default
# gdu:localidad + manzana/calle/vivienda_punto) vía REST, y configura el
# subsistema de seguridad (servicio de roles JDBC respaldado por Django,
# reglas de Data Access) escribiendo directamente los archivos del data dir
# -- porque la API REST de GeoServer no cubre servicios de roles ni reglas de
# acceso a datos, solo workspaces/datastores/capas.
#
# Reproduce exactamente lo que se validó a mano en el piloto local (ver
# /home/willy/.claude/plans/wfs-t-geoserver-qgis-gdu.md, Fase 1 y 2): el mismo
# contrato SQL para el servicio de roles JDBC, el mismo bridge admin->ADMIN
# (sin el cual activar este servicio de roles deja sin acceso al admin de
# GeoServer), y las mismas Data Access Rules probadas con anónimo/viewer/admin.
#
# Este script asume que la fase "geoserver" corre en el MISMO servidor que
# Postgres (GeoServer nativo comparte el namespace de red del host, así que
# PGHOST puede ser 127.0.0.1 sin tocar pg_hba.conf -- a diferencia del
# GeoServer en Docker que se usaba antes, que necesitaba la IP LAN real del
# host para llegar a Postgres desde su red bridge). La fase "postgres"
# también corre ahí: el paso que necesita superusuario (CREATE ROLE) usa
# `sudo -u postgres psql` por socket local (peer auth), no por TCP -- igual
# que migrar_gdu_a_produccion.sh. Motivo: tanto en dev como en producción el
# rol `postgres` no tiene contraseña seteada (solo peer auth local), así que
# exigir una hubiera significado fijarle una contraseña a un superusuario y
# abrir pg_hba.conf a auth por TCP para ese rol -- innecesario cuando el
# script de todos modos se corre en el propio servidor de Postgres. El resto
# (schema geoserver_auth como PG_APP_USER) sigue conectando siempre por TCP
# con usuario y contraseña.
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
#   ./deploy_geoserver.sh geoserver  # instala/actualiza el servicio nativo de GeoServer
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
GEOSERVER_VERSION="${GEOSERVER_VERSION:-2.26.2}"
# Puerto del conector HTTP de Jetty (jetty.http.port en start.ini) -- a
# diferencia del `-p` de Docker, cambiarlo de 8080 hace que
# write_geoserver_systemd_unit agregue -Djetty.http.port=... a JAVA_OPTS
# (ver más abajo); esta variable también define a qué puerto le pega el
# propio script (GEOSERVER_URL).
GEOSERVER_HTTP_PORT="${GEOSERVER_HTTP_PORT:-8080}"
GEOSERVER_DATA_DIR="${GEOSERVER_DATA_DIR:-/opt/geoserver_data}"
GEOSERVER_ADMIN_USER="${GEOSERVER_ADMIN_USER:-admin}"
GEOSERVER_URL="${GEOSERVER_URL:-http://127.0.0.1:${GEOSERVER_HTTP_PORT}/geoserver}"
PGPORT="${PGPORT:-5432}"

# GeoServer standalone (distribución "bin" oficial, Jetty 9.4 embebido) --
# NO Tomcat. Se probó primero con el paquete apt "tomcat10" (Ubuntu ya no
# empaqueta tomcat9) y falló en caliente: el WAR de GeoServer 2.26.2 está
# compilado contra el namespace viejo `javax.servlet.*` (Servlet 4), y
# Tomcat 10 solo trae `jakarta.servlet.*` -- ClassNotFoundException:
# javax.servlet.http.HttpSessionListener, confirmado en los logs reales.
# La distribución "bin" de GeoServer trae su propio Jetty 9.4 con
# javax.servlet-api-3.1.0.jar embebido, así que no depende de qué servlet
# container tenga el sistema -- mismo enfoque que la imagen Docker (que
# tampoco usaba el Tomcat del sistema, traía el suyo propio).
GEOSERVER_HOME="${GEOSERVER_HOME:-/opt/geoserver}"
GEOSERVER_SERVICE_USER="${GEOSERVER_SERVICE_USER:-geoserver}"
GEOSERVER_SYSTEMD_SERVICE="${GEOSERVER_SYSTEMD_SERVICE:-geoserver}"
GEOSERVER_WEBAPP_DIR="$GEOSERVER_HOME/webapps/geoserver"

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
  # caliente) o directo una página de error 401 del servlet container sin
  # ese texto (típico después de un restart completo, visto en vivo al
  # generalizar a plano_mensura/tierra) -- se acepta cualquiera de las dos
  # en vez de depender de un único formato de respuesta.
  local typename="$1" code body
  code="$(curl -s -o "$REST_BODY_FILE" -w '%{http_code}' "${GEOSERVER_URL}/${GS_WORKSPACE}/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=${typename}&count=1")"
  body="$(cat "$REST_BODY_FILE" 2>/dev/null)"
  [[ "$code" == "401" || "$code" == "403" || "$body" == *"unknown"* || "$body" == *"Exception"* ]]
}

phase_postgres() {
  log "Fase Postgres: creando roles (necesita superusuario) y schema geoserver_auth"
  require_env PGDATABASE
  require_env PG_APP_USER
  require_env PG_APP_PASSWORD
  require_env GEOSERVER_DS_PASSWORD
  require_env GEOSERVER_SECURITY_DB_PASSWORD

  render_template "$SQL_DIR/01_provision_roles.sql.tmpl" "$RENDERED_DIR/01_provision_roles.sql" \
    GEOSERVER_DS_PASSWORD GEOSERVER_SECURITY_DB_PASSWORD

  log "Aplicando 01_provision_roles.sql como postgres via sudo (CREATE ROLE, peer auth local -- ver comentario al inicio del script)..."
  # -f no sirve acá: el usuario postgres normalmente no puede atravesar el
  # $HOME de quien corre el script (ej. /home/willy es 750) para llegar al
  # archivo renderizado. Redirigiendo por stdin, el shell abre el archivo
  # con los permisos de quien invoca sudo (antes de escalar), y el
  # descriptor ya abierto se hereda al proceso hijo -- sin depender de que
  # postgres tenga acceso al filesystem del caller.
  sudo -u postgres psql -d "$PGDATABASE" \
    -v ON_ERROR_STOP=1 < "$RENDERED_DIR/01_provision_roles.sql"

  log "Aplicando 02_provision_schema.sql como $PG_APP_USER (schema geoserver_auth + grants)..."
  PGPASSWORD="$PG_APP_PASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PG_APP_USER" -d "$PGDATABASE" \
    -v ON_ERROR_STOP=1 -f "$SQL_DIR/02_provision_schema.sql"

  log "Fase Postgres OK"
}

provision_geoserver_native() {
  log "Asegurando GeoServer $GEOSERVER_VERSION instalado nativamente (standalone, Jetty embebido)..."

  command -v unzip >/dev/null || sudo apt-get install -y unzip
  id -u "$GEOSERVER_SERVICE_USER" >/dev/null 2>&1 || \
    sudo useradd --system --no-create-home --home-dir "$GEOSERVER_HOME" --shell /usr/sbin/nologin "$GEOSERVER_SERVICE_USER"

  # Idempotente: compara la versión ya desplegada (si la hay) contra
  # GEOSERVER_VERSION vía $GEOSERVER_HOME/VERSION.txt, en vez de asumir por
  # la sola presencia del directorio. OJO: la distribución "bin" (a
  # diferencia del WAR) no trae META-INF/MANIFEST.MF en webapps/geoserver --
  # confirmado en vivo, VERSION.txt es la única fuente confiable acá.
  local deployed_version=""
  if [[ -f "$GEOSERVER_HOME/VERSION.txt" ]]; then
    deployed_version="$(sudo grep -m1 '^version = ' "$GEOSERVER_HOME/VERSION.txt" 2>/dev/null | awk '{print $3}')"
  fi
  if [[ "$deployed_version" != "$GEOSERVER_VERSION" ]]; then
    log "Desplegando GeoServer $GEOSERVER_VERSION (distribución bin oficial, reemplaza versión previa '${deployed_version:-ninguna}')..."
    local bin_zip="$RENDERED_DIR/geoserver-${GEOSERVER_VERSION}-bin.zip"
    # -C - --retry: SourceForge cierra la conexión a mitad de descarga con
    # cierta frecuencia (~100MB+ el zip) -- confirmado en vivo, un curl -sfL
    # simple cortaba a los ~30-60MB. Resume + reintentos lo resuelve.
    curl -sfL -C - --retry 5 --retry-delay 3 "https://downloads.sourceforge.net/project/geoserver/GeoServer/${GEOSERVER_VERSION}/geoserver-${GEOSERVER_VERSION}-bin.zip" -o "$bin_zip"
    sudo systemctl stop "$GEOSERVER_SYSTEMD_SERVICE" 2>/dev/null || true
    # data_dir/ del zip es la data dir de EJEMPLO que trae GeoServer -- no la
    # usamos (GEOSERVER_DATA_DIR apunta a $GEOSERVER_DATA_DIR, fuera de
    # $GEOSERVER_HOME), así que no hace falta extraerla ni preservarla.
    sudo rm -rf "$GEOSERVER_HOME"
    sudo mkdir -p "$GEOSERVER_HOME"
    sudo unzip -o -q "$bin_zip" -x 'data_dir/*' -d "$GEOSERVER_HOME"
    sudo chmod +x "$GEOSERVER_HOME/bin/"*.sh
    sudo chown -R "${GEOSERVER_SERVICE_USER}:${GEOSERVER_SERVICE_USER}" "$GEOSERVER_HOME"
  else
    log "GeoServer $GEOSERVER_VERSION ya desplegado en $GEOSERVER_HOME, no se toca"
  fi

  # marlin.jar (renderer JAI acelerado, committeado en plugin/marlin.jar -- no
  # viene en la distribución de GeoServer, lo agregaba la imagen Docker) va
  # en $GEOSERVER_HOME/webapps/ (NO dentro de webapps/geoserver/, así
  # sobrevive un redeploy de versión que borra y re-extrae ese subdirectorio)
  # -- bin/startup.sh lo detecta solo ahí (`find webapps -name "marlin*.jar"`)
  # y lo activa vía --patch-module, sin que este script tenga que tocar
  # JAVA_OPTS para eso.
  log "Instalando marlin.jar (renderer JAI acelerado)..."
  sudo cp "$PLUGIN_DIR/marlin.jar" "$GEOSERVER_HOME/webapps/marlin.jar"
  sudo chown "${GEOSERVER_SERVICE_USER}:${GEOSERVER_SERVICE_USER}" "$GEOSERVER_HOME/webapps/marlin.jar"

  sudo mkdir -p "$GEOSERVER_DATA_DIR"
  sudo chown -R "${GEOSERVER_SERVICE_USER}:${GEOSERVER_SERVICE_USER}" "$GEOSERVER_DATA_DIR"

  write_geoserver_systemd_unit
  sudo systemctl enable "$GEOSERVER_SYSTEMD_SERVICE" >/dev/null 2>&1 || true
  sudo systemctl restart "$GEOSERVER_SYSTEMD_SERVICE"
}

write_geoserver_systemd_unit() {
  # No hay paquete de sistema para esta distribución (es un zip standalone),
  # así que el unit es nuestro, no de un paquete apt -- se sobreescribe
  # entero en cada corrida a propósito (no hay nada del sistema que
  # preservar, a diferencia de /etc/default/tomcat10 en el intento anterior).
  #
  # bin/startup.sh (ver el propio script) ya trae hardcodeados todos los
  # --add-opens/--add-exports que la imagen Docker pasaba a mano por
  # CATALINA_OPTS, y detecta marlin.jar solo -- JAVA_OPTS acá solo necesita
  # el heap y el flag de GeoTools que no vienen por default.
  local java_opts="-Xms256m -Xmx1g -Dorg.geotools.coverage.jaiext.enabled=true"
  [[ "$GEOSERVER_HTTP_PORT" != "8080" ]] && java_opts="$java_opts -Djetty.http.port=${GEOSERVER_HTTP_PORT}"

  cat > "$RENDERED_DIR/geoserver.service" <<EOF
[Unit]
Description=GeoServer (WFS-T / GDU) -- gestionado por deploy_geoserver.sh, no editar a mano
After=network.target postgresql.service

[Service]
Type=simple
User=${GEOSERVER_SERVICE_USER}
Group=${GEOSERVER_SERVICE_USER}
Environment=GEOSERVER_HOME=${GEOSERVER_HOME}
Environment=GEOSERVER_DATA_DIR=${GEOSERVER_DATA_DIR}
Environment=JAVA_OPTS=${java_opts}
WorkingDirectory=${GEOSERVER_HOME}
ExecStart=${GEOSERVER_HOME}/bin/startup.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
  sudo cp "$RENDERED_DIR/geoserver.service" "/etc/systemd/system/${GEOSERVER_SYSTEMD_SERVICE}.service"
  sudo systemctl daemon-reload
}

bootstrap_admin_password() {
  # Esta versión de GeoServer YA NO usa admin/geoserver como default de
  # fábrica (confirmado en vivo, no es una suposición): en un data dir
  # fresco genera una contraseña de admin ALEATORIA que nunca se revela en
  # texto plano en ningún lado (a diferencia de la master password, que sí
  # queda legible una vez en security/masterpw.info). La única puerta de
  # entrada disponible es habilitar temporalmente el login con master
  # password (usuario sintético "root", ver security/masterpw/default/
  # config.xml -- <loginEnabled> viene en false por default), autenticar con
  # eso, y rotar la contraseña de admin por REST. Este paso es idempotente:
  # en corridas siguientes GEOSERVER_ADMIN_USER ya autentica con la
  # contraseña deseada y se sale en el primer chequeo. Asume
  # GEOSERVER_ADMIN_USER=admin (el username que GeoServer crea solo al
  # inicializar el data dir) -- si se cambia a otro usuario, este bootstrap
  # no alcanza y hay que crearlo a mano.
  log "Verificando credenciales de $GEOSERVER_ADMIN_USER..."
  local code
  code="$(curl -s -o /dev/null -w '%{http_code}' -u "${GEOSERVER_ADMIN_USER}:${GEOSERVER_ADMIN_PASSWORD}" "${GEOSERVER_URL}/rest/about/version.json")"
  if [[ "$code" == "200" ]]; then
    log "OK: $GEOSERVER_ADMIN_USER ya autentica con la contraseña deseada"
    return
  fi

  local masterpw_info="$GEOSERVER_DATA_DIR/security/masterpw.info"
  sudo test -f "$masterpw_info" || die "$GEOSERVER_ADMIN_USER no autenticó y no existe $masterpw_info para el fallback de master password -- revisar $GEOSERVER_DATA_DIR/security/usergroup/default/users.xml a mano."
  local masterpw
  masterpw="$(sudo grep -oP 'generated master password is: \K.*' "$masterpw_info")"
  [[ -n "$masterpw" ]] || die "No se pudo leer la master password generada de $masterpw_info"

  log "Habilitando temporalmente el login con master password (usuario root) para rotar la contraseña de admin por primera vez..."
  local masterpw_config="$GEOSERVER_DATA_DIR/security/masterpw/default/config.xml"
  sudo sed -i 's#<loginEnabled>false</loginEnabled>#<loginEnabled>true</loginEnabled>#' "$masterpw_config"
  sudo systemctl restart "$GEOSERVER_SYSTEMD_SERVICE"
  wait_for_geoserver

  code="$(curl -s -o /dev/null -w '%{http_code}' -u "root:${masterpw}" "${GEOSERVER_URL}/rest/about/version.json")"
  [[ "$code" == "200" ]] || die "root con la master password no autenticó (HTTP $code) después de habilitar loginEnabled -- revisar $masterpw_config a mano."

  printf '<user><password>%s</password></user>' "$GEOSERVER_ADMIN_PASSWORD" > "$RENDERED_DIR/admin-password.xml"
  local rest_code
  rest_code="$(curl -s -o "$REST_BODY_FILE" -w '%{http_code}' -u "root:${masterpw}" -X POST -H "Content-Type: application/xml" --data-binary "@$RENDERED_DIR/admin-password.xml" "${GEOSERVER_URL}/rest/security/usergroup/user/${GEOSERVER_ADMIN_USER}")"
  case "$rest_code" in
    2??) log "OK: contraseña de $GEOSERVER_ADMIN_USER actualizada" ;;
    *) die "No se pudo rotar la contraseña de admin -> HTTP $rest_code: $(cat "$REST_BODY_FILE" 2>/dev/null)" ;;
  esac

  # Vuelve a deshabilitar el login con master password en el archivo -- no
  # hace falta otro restart acá para que surta efecto: overlay_security_config
  # (que corre siempre a continuación dentro de phase_geoserver) ya reinicia
  # GeoServer por su cuenta, y ese restart levanta el archivo con el valor
  # ya revertido a false.
  sudo sed -i 's#<loginEnabled>true</loginEnabled>#<loginEnabled>false</loginEnabled>#' "$masterpw_config"
}

overlay_security_config() {
  log "Escribiendo configuración de seguridad en el data dir de GeoServer..."
  require_env PGHOST
  require_env PGDATABASE
  require_env GEOSERVER_SECURITY_DB_PASSWORD

  render_template "$TEMPLATES_DIR/role-service-config.xml.tmpl" "$RENDERED_DIR/role-service-config.xml" \
    PGHOST PGPORT PGDATABASE GEOSERVER_SECURITY_DB_PASSWORD

  sudo mkdir -p "$GEOSERVER_DATA_DIR/security/role/django"
  sudo cp "$RENDERED_DIR/role-service-config.xml" "$GEOSERVER_DATA_DIR/security/role/django/config.xml"
  sudo cp "$TEMPLATES_DIR/rolesddl.xml" "$GEOSERVER_DATA_DIR/security/role/django/rolesddl.xml"
  sudo cp "$TEMPLATES_DIR/roles-django.dml.xml" "$GEOSERVER_DATA_DIR/security/role/django/roles-django.dml.xml"
  sudo cp "$TEMPLATES_DIR/layers.properties" "$GEOSERVER_DATA_DIR/security/layers.properties"

  # OJO: a diferencia de todo lo anterior en esta función, este jar NO va al
  # data dir persistente ($GEOSERVER_DATA_DIR), va al WEB-INF/lib del webapp
  # -- por eso se copia acá en cada corrida (idempotente, se sobreescribe) en
  # vez de una sola vez: si se redespliega desde cero (nueva versión de
  # GeoServer), WEB-INF/lib vuelve a como venía de fábrica y no incluye este
  # plugin.
  log "Instalando plugin gdu-updated-by-listener.jar (updated_by por usuario autenticado)..."
  sudo cp "$PLUGIN_DIR/gdu-updated-by-listener.jar" "$GEOSERVER_WEBAPP_DIR/WEB-INF/lib/gdu-updated-by-listener.jar"

  if [[ -n "${LDAP_BIND_DN:-}" && -n "${LDAP_BIND_PASSWORD:-}" ]]; then
    log "Configurando proveedor de autenticación LDAP ($LDAP_PROVIDER_NAME)..."
    render_template "$TEMPLATES_DIR/ldap-auth-config.xml.tmpl" "$RENDERED_DIR/ldap-auth-config.xml" \
      LDAP_PROVIDER_NAME LDAP_SERVER_URL LDAP_USER_FILTER LDAP_USER_NAME_ATTRIBUTE LDAP_BIND_DN LDAP_BIND_PASSWORD
    sudo mkdir -p "$GEOSERVER_DATA_DIR/security/auth/${LDAP_PROVIDER_NAME}"
    sudo cp "$RENDERED_DIR/ldap-auth-config.xml" "$GEOSERVER_DATA_DIR/security/auth/${LDAP_PROVIDER_NAME}/config.xml"
    EXTRA_AUTH_PROVIDERS="<string>${LDAP_PROVIDER_NAME}</string>"
  else
    log "LDAP_BIND_DN/LDAP_BIND_PASSWORD no definidos -- se omite el proveedor LDAP, queda solo 'default' (admin local)"
    EXTRA_AUTH_PROVIDERS=""
  fi
  render_template "$TEMPLATES_DIR/security-config.xml.tmpl" "$RENDERED_DIR/security-config.xml" EXTRA_AUTH_PROVIDERS
  sudo cp "$RENDERED_DIR/security-config.xml" "$GEOSERVER_DATA_DIR/security/config.xml"

  sudo chown -R "${GEOSERVER_SERVICE_USER}:${GEOSERVER_SERVICE_USER}" "$GEOSERVER_DATA_DIR/security" "$GEOSERVER_WEBAPP_DIR/WEB-INF/lib/gdu-updated-by-listener.jar"

  log "Reiniciando GeoServer para que tome la config de seguridad (un simple /rest/reload no alcanza para el servicio de roles JDBC ni para un proveedor de autenticación nuevo -- confirmado a mano en el piloto)..."
  sudo systemctl restart "$GEOSERVER_SYSTEMD_SERVICE"
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

  provision_geoserver_native
  wait_for_geoserver 180
  bootstrap_admin_password
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
