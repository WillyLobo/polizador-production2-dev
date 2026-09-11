# Deploy de GeoServer (WFS-T / GDU)

Automatiza en un servidor nuevo lo que se validó a mano en el piloto local
(ver `/home/willy/.claude/plans/wfs-t-geoserver-qgis-gdu.md`, Fases 1 y 2):
GeoServer como servicio **nativo** (distribución "bin" standalone oficial,
Jetty 9.4 embebido, gestionado por un unit de systemd propio -- sin Docker,
sin depender de ningún servlet container del sistema) publicando
`gdu:localidad` vía WFS-T, con un servicio de roles JDBC que lee en vivo los
`Group` de Django (vía Postgres) y reglas de Data Access Rules que usan esos
roles.

**Por qué la distribución "bin" y no un WAR en Tomcat:** se probó primero
desplegar el WAR de GeoServer en el `tomcat10` de Ubuntu y falló en
caliente -- el WAR de GeoServer 2.26.2 está compilado contra el namespace
viejo `javax.servlet.*` (Servlet 4), y Tomcat 10 solo trae
`jakarta.servlet.*` (`ClassNotFoundException:
javax.servlet.http.HttpSessionListener`, confirmado en los logs reales).
Ubuntu ya no empaqueta `tomcat9` (el que sí matchea). La distribución "bin"
de GeoServer trae su propio Jetty 9.4 con `javax.servlet-api-3.1.0.jar`
embebido, así que no depende de qué servlet container tenga el sistema --
mismo enfoque que la imagen Docker que se usaba antes (que tampoco usaba el
Tomcat del sistema, traía el suyo propio).

GeoServer corre en el **mismo servidor que Postgres**: comparte el namespace
de red del host, así que `PGHOST` puede ser `127.0.0.1` sin necesitar reglas
nuevas en `pg_hba.conf` (a diferencia de un GeoServer en Docker con red
bridge, que necesitaría la IP LAN real del host para llegar a Postgres). El
paso de la fase `postgres` que necesita superusuario (`CREATE ROLE`) corre
como `sudo -u postgres psql` por socket local (peer auth), igual que
`migrar_gdu_a_produccion.sh` -- porque tanto en dev como en producción el rol
`postgres` no tiene contraseña seteada, y exigir una hubiera significado
fijarle una y abrir `pg_hba.conf` a auth por TCP para un superusuario sin
necesidad real. Tanto `postgres` como `geoserver` requieren correrse en ese
mismo servidor (con sudo habilitado hacia `postgres` y hacia la
instalación/gestión del servicio `geoserver`). El schema `geoserver_auth`
como `PG_APP_USER` sigue conectando por TCP con usuario/contraseña, igual
que antes.

## Qué automatiza y qué no

- Automatiza: instalar/actualizar GeoServer nativo (distribución "bin"
  oficial, un usuario de sistema dedicado, un unit de systemd propio -- sin
  paquete apt ni Docker de por medio), crear roles/schema en Postgres,
  publicar workspace/datastore/capa por REST, configurar el servicio de
  roles JDBC y las Data Access Rules (escribiendo archivos del data dir
  directamente, ya que la REST API de GeoServer no cubre seguridad), LDAP
  como proveedor de autenticación (opcional, ver "Variables de entorno"), y
  el plugin que completa `updated_by` con el usuario autenticado real (ver
  más abajo).
- Deliberadamente NO automatiza: reconectar el proyecto QGIS (Fase 3, script
  aparte en `qgis-gdu/`), ni generalizar a más capas (Fase 4, hoy solo
  `localidad`).
- Alcance actual: una sola capa piloto (`gdu:localidad`). Sumar otra capa es
  editar `GS_FEATURETYPE`/la sección de grants en `sql/02_provision_schema.sql`
  y las reglas en `templates/layers.properties` -- no hace falta tocar la
  lógica del script.

## Decisión importante: contraseñas de configuración en texto plano

El piloto local usaba cifrado PBE (la config por default de GeoServer) para
la contraseña del datastore y del servicio de roles JDBC. Ese cifrado está
atado a la master key de ESE proceso de GeoServer -- no es portable a un
servidor nuevo sin generar la master key ahí y volver a cifrar a mano (rompe
la automatización). Este script cambia la política global a
`plainTextPasswordEncoder` (`templates/security-config.xml`,
`configPasswordEncrypterName`) para poder templatizar el `config.xml` del
servicio de roles con una contraseña real y que arranque funcionando en
cualquier servidor, sin pasos manuales por la UI.

Mitigación: restringir el acceso al filesystem del data dir
(`GEOSERVER_DATA_DIR`, propiedad del usuario de sistema `geoserver`) -- quien
tenga acceso de lectura ahí puede ver las contraseñas en texto plano. Es el
mismo nivel de exposición que ya existía (`geoserver_piloto`/
`geoserver_security` son roles Postgres de bajísimo privilegio, no la
contraseña de un superusuario ni de ningún usuario real de Django/LDAP).

## Variables de entorno

Ninguna tiene un default "real" para lo que es específico del servidor de
destino o un secreto -- el script corta con un mensaje claro si falta alguna.

### GeoServer nativo (fase `geoserver`)

| Variable | Default | Descripción |
|---|---|---|
| `GEOSERVER_ADMIN_PASSWORD` | *(requerida)* | Contraseña deseada para el admin de GeoServer. En un data dir nuevo, el script la rota una sola vez desde la contraseña aleatoria de fábrica -- ver "Bootstrap de la contraseña de admin" más abajo |
| `GEOSERVER_ADMIN_USER` | `admin` | Usuario admin de GeoServer -- el bootstrap de contraseña asume que es `admin` (el username que GeoServer crea solo al inicializar el data dir) |
| `GEOSERVER_VERSION` | `2.26.2` | Versión de GeoServer a instalar (distribución "bin" oficial de SourceForge) |
| `GEOSERVER_HTTP_PORT` | `8080` | Puerto del conector HTTP de Jetty (`jetty.http.port` en `start.ini`). Cambiarlo de 8080 hace que el script agregue `-Djetty.http.port=...` a `JAVA_OPTS` del unit de systemd -- no hay mapeo `-p` como con Docker |
| `GEOSERVER_DATA_DIR` | `/opt/geoserver_data` | Directorio del data dir de GeoServer (antes `GEOSERVER_DATA_DIR_HOST`, era el bind mount de Docker) |
| `GEOSERVER_URL` | `http://127.0.0.1:$GEOSERVER_HTTP_PORT/geoserver` | Base URL para las llamadas REST del propio script -- cambiar si se corre remoto |
| `GEOSERVER_HOME` | `/opt/geoserver` | Dónde se instala la distribución "bin" de GeoServer (binarios, `start.jar`, `webapps/geoserver/`) |
| `GEOSERVER_SERVICE_USER` | `geoserver` | Usuario de sistema dedicado que corre el proceso (el script lo crea si no existe, `--system --no-create-home`) |
| `GEOSERVER_SYSTEMD_SERVICE` | `geoserver` | Nombre del unit de systemd (`/etc/systemd/system/$GEOSERVER_SYSTEMD_SERVICE.service`, generado por el script) |

### Postgres (fases `postgres` y `geoserver`)

| Variable | Default | Descripción |
|---|---|---|
| `PGHOST` | *(requerida, salvo fase `postgres`)* | Host de Postgres -- típicamente `127.0.0.1`, ya que GeoServer corre en el mismo servidor |
| `PGPORT` | `5432` | Puerto de Postgres |
| `PGDATABASE` | *(requerida)* | Base de datos destino |
| `PG_APP_USER` / `PG_APP_PASSWORD` | *(requeridas, solo fase `postgres`)* | Credenciales con privilegio para crear el schema `geoserver_auth` y hacer GRANT sobre `catastro.*` (ej. el `DBUSER` de `polizador/.env`) |
| `GEOSERVER_DS_PASSWORD` | *(requerida)* | Contraseña a fijar/usar para el rol `geoserver_piloto` (datastore) |
| `GEOSERVER_SECURITY_DB_PASSWORD` | *(requerida)* | Contraseña a fijar/usar para el rol `geoserver_security` (servicio de roles) |

### Identificadores del workspace/capa piloto (rara vez hace falta tocarlos)

`GS_WORKSPACE=gdu`, `GS_DATASTORE=catastro`, `GS_NAMESPACE_URI=http://gdu`,
`GS_PG_SCHEMA=catastro`, `GS_FEATURETYPE=localidad`,
`GS_FEATURETYPE_SRS=EPSG:22175`.

### LDAP (autenticación -- opcional, fase `geoserver`)

Si no se definen `LDAP_BIND_DN`/`LDAP_BIND_PASSWORD`, se omite por completo
(el proveedor sigue siendo solo `default`, igual que hasta ahora). Cuando se
definen, agrega un proveedor de autenticación LDAP contra el mismo AD que ya
usa Django -- ver la explicación completa más abajo, en "Pendiente".

| Variable | Default | Descripción |
|---|---|---|
| `LDAP_BIND_DN` | *(sin default, opcional)* | Cuenta de bind para la búsqueda, ej. `IPDUV\admindeu` (mismo valor que `GDU_LDAP_BIND_DN` en `polizador/.env`) |
| `LDAP_BIND_PASSWORD` | *(sin default, opcional)* | Contraseña de esa cuenta (mismo valor que `GDU_LDAP_BIND_CREDENTIALS`) |
| `LDAP_SERVER_URL` | `ldap://10.106.16.3:389/dc=ipduv,dc=gov,dc=ar` | Tiene default porque es infraestructura fija de IPDUV, no un secreto |
| `LDAP_USER_FILTER` | `(sAMAccountName={0})` | Filtro de búsqueda (mismo patrón que `GDU_LDAP_SEARCH_FILTER`, con `{0}` en vez de `{{username}}`) |
| `LDAP_USER_NAME_ATTRIBUTE` | `sAMAccountName` | |
| `LDAP_PROVIDER_NAME` | `ldap-ipduv` | Nombre del proveedor (define el directorio `security/auth/<nombre>/` y la entrada en `authProviderNames`) |

## Uso

Con `export` directo en el shell:

```bash
export GEOSERVER_ADMIN_PASSWORD='...'
export PGHOST=... PGDATABASE=...
export PG_APP_USER=... PG_APP_PASSWORD='...'
export GEOSERVER_DS_PASSWORD='...' GEOSERVER_SECURITY_DB_PASSWORD='...'

./deploy_geoserver.sh postgres    # roles + schema geoserver_auth en Postgres -- correr en el server de Postgres, pide sudo hacia el usuario postgres
./deploy_geoserver.sh geoserver   # instala/actualiza GeoServer + workspace/datastore/capa + seguridad
./deploy_geoserver.sh verify      # repite la batería de pruebas allow/deny de la Fase 2
```

O en un archivo `geoserver/.env` (mismo patrón que `polizador/.env`, pero acá
lo carga el propio script, no django-environ): si existe, `deploy_geoserver.sh`
lo sourcea automáticamente antes de correr cualquier fase. No se versiona
(ver `.gitignore`) porque son secretos y valores de un servidor de destino
puntual.

```bash
# geoserver/.env
GEOSERVER_ADMIN_PASSWORD='...'
PGHOST=...
PGDATABASE=...
PG_APP_USER=...
PG_APP_PASSWORD='...'
GEOSERVER_DS_PASSWORD='...'
GEOSERVER_SECURITY_DB_PASSWORD='...'
```

```bash
./deploy_geoserver.sh postgres
./deploy_geoserver.sh geoserver
./deploy_geoserver.sh verify
```

Sin `export` y sin comillas alrededor de valores con espacios -- el script
hace `source` del archivo tal cual, así que las reglas son las de bash
normal (comillas simples para valores literales, sin `$` sin escapar salvo
que la expansión sea intencional).

`postgres` corre siempre en el propio servidor de Postgres (necesita sudo
local hacia el usuario `postgres`, ver arriba); `geoserver` se puede correr
desde una máquina distinta (la que va a instalar/correr el servicio nativo)
-- cada fase pide solo las variables que necesita. `all` corre las tres
fases en orden en la misma máquina, y por lo tanto asume que esa máquina es
también el servidor de Postgres.

Todo es re-ejecutable: los roles de Postgres se crean con `ALTER ROLE` si ya
existen, las vistas se recrean con `DROP VIEW IF EXISTS`, el workspace/
datastore/capa se consultan antes de crear (se saltean si ya existen, o se
actualiza el datastore si cambió algún parámetro de conexión), y los archivos
de seguridad simplemente se sobreescriben.

La fase `geoserver` necesita `sudo` real (crea el usuario de sistema
`geoserver` si no existe, descarga y despliega la distribución "bin" de
GeoServer en `$GEOSERVER_HOME`, escribe `$GEOSERVER_DATA_DIR` y el unit de
systemd, y reinicia el servicio) y acceso a internet la primera vez, para
bajar `geoserver-$GEOSERVER_VERSION-bin.zip` de SourceForge (~113MB;
SourceForge corta la conexión a mitad de descarga con cierta frecuencia --
el script usa `curl -C - --retry` para resumir en vez de fallar de una).

## Bootstrap de la contraseña de admin

A diferencia de la imagen Docker que se usaba antes (que reescribía
`security/usergroup/default/users.xml` con `GEOSERVER_ADMIN_USER`/
`GEOSERVER_ADMIN_PASSWORD` en cada arranque del contenedor), y a diferencia
de versiones viejas de GeoServer (que arrancaban con `admin`/`geoserver` de
fábrica), esta versión de GeoServer en un data dir recién inicializado
genera una contraseña de admin **aleatoria que nunca se revela en texto
plano en ningún lado** -- confirmado en vivo, no es una suposición. Lo único
que sí queda legible una vez es la master password, en
`$GEOSERVER_DATA_DIR/security/masterpw.info` (borrable después de leída).

`deploy_geoserver.sh geoserver` compensa esto con un paso de bootstrap
(`bootstrap_admin_password`, antes de `overlay_security_config`):
1. Si `GEOSERVER_ADMIN_USER`/`GEOSERVER_ADMIN_PASSWORD` ya autentican, no
   hace nada (caso normal en corridas siguientes).
2. Si no, lee la master password de `security/masterpw.info` y habilita
   temporalmente `<loginEnabled>true</loginEnabled>` en
   `security/masterpw/default/config.xml` (viene en `false` por default --
   sin esto, ni siquiera el usuario sintético `root` con la master password
   correcta autentica, confirmado en vivo: daba 401 hasta habilitarlo).
3. Reinicia GeoServer para que tome ese cambio, autentica como
   `root:<master password>` por REST, y rota la contraseña del usuario
   `admin` (`POST /rest/security/usergroup/user/admin`).
4. Vuelve a dejar `loginEnabled` en `false` en el archivo -- no hace falta
   otro restart para que surta efecto, el que ya hace
   `overlay_security_config` a continuación lo levanta con el valor ya
   revertido.

Asume `GEOSERVER_ADMIN_USER=admin` (el username que GeoServer crea solo al
inicializar el data dir); si se necesita otro username hay que crearlo a
mano.

## `updated_by` por fila: plugin `gdu-updated-by-listener.jar`

El datastore de GeoServer escribe siempre con la misma credencial de
conexión (`geoserver_piloto`) -- sin nada más, cualquier `INSERT`/`UPDATE`
por WFS-T queda con `updated_by = 'geoserver_piloto'` en Postgres, sin
distinguir usuarios reales, y confiar en lo que el cliente WFS-T mande en esa
columna es inseguro (cualquiera puede mandar cualquier nombre). `plugin/`
tiene una extensión Java chica de GeoServer que reemplaza el valor de
`updated_by`/`updated_at` por el usuario realmente autenticado (LDAP o
`admin`) en cada Insert/Update, antes de que la transacción llegue a
Postgres.

**Cómo funciona:** implementa `org.geoserver.ows.DispatcherCallback`
(`operationDispatched`), no `TransactionListener` -- ese fue el primer
intento y no tuvo ningún efecto: se confirmó contra el código fuente real de
GeoServer (`UpdateElementHandler.execute()`, rama 2.26.x) que el array de
valores que se le pasa a `FeatureStore.modifyFeatures()` se arma ANTES de
disparar el evento `PRE_UPDATE` que recibe un `TransactionListener`, así que
para cuando el listener corre ya es tarde para cambiar nada. `operationDispatched`
en cambio corre antes de que el Dispatcher invoque la operación, así que
alcanza a editar el `TransactionType` (el request WFS-T ya parseado, con sus
elementos Insert/Update) a tiempo tanto para inserts como para updates.

**Requiere el trigger con `COALESCE`** (`sql/02_provision_schema.sql`,
`catastro.set_updated()`): sin eso, el trigger pisa `updated_by` con
`current_user` igual, sin importar lo que haya puesto el plugin. Ese mismo
trigger es compartido por ~30 tablas de `catastro`, así que el fix aplica a
todas aunque hoy solo `localidad` pase por WFS-T.

**Build:** el jar ya está compilado y commiteado (`plugin/gdu-updated-by-listener.jar`,
~3KB). Si cambia la versión de GeoServer, recompilar con `plugin/build.sh`
(sin argumentos usa `/opt/geoserver/webapps/geoserver/WEB-INF/lib`, o pasar
otra ruta) -- compila contra el classpath real de un GeoServer ya desplegado
(`sudo cp` de su `WEB-INF/lib`, es del usuario de sistema `geoserver`), no
usa Maven porque no hay Maven instalado en el entorno de desarrollo donde se
escribió esto por primera vez. `deploy_geoserver.sh` lo copia a `WEB-INF/lib`
en cada corrida de `geoserver` (no al data dir persistente -- si se
redespliega desde cero por un cambio de versión, `WEB-INF/lib` vuelve a como
venía de fábrica).

`plugin/marlin.jar` (renderer JAI acelerado, ~190KB, también commiteado) no
tiene que ver con este plugin -- lo instala `deploy_geoserver.sh` en
`$GEOSERVER_HOME/webapps/marlin.jar` (NO dentro de `webapps/geoserver/`, así
sobrevive un redeploy de versión) porque la imagen Docker que se usaba antes
lo agregaba por su cuenta, y la distribución oficial de GeoServer no lo
incluye. A diferencia del enfoque Docker (que necesitaba
`-Xbootclasspath/a:...` + `-Dsun.java2d.renderer=...` a mano),
`bin/startup.sh` de esta distribución ya busca `marlin*.jar` en `webapps/`
solo y lo activa vía `--patch-module` -- no hace falta que
`deploy_geoserver.sh` toque `JAVA_OPTS` para esto.

Validado en el piloto: un `Update` que manda `updated_by=deploy_verify`
explícitamente en el WFS-T (`phase_verify` lo hace a propósito) queda en
Postgres como `updated_by=admin` -- confirma que el plugin gana, no el valor
del cliente.

**Bug real encontrado y corregido (2026-09-10):** el camino de `Insert` ya
chequeaba si el feature type tenía `updated_by` antes de tocarlo
(`SimpleFeature.getFeatureType().getDescriptor()`), pero el camino de
`Update` (`setOrReplaceProperty`) no -- le agregaba `updated_by`/`updated_at`
a CUALQUIER `Update`, sin importar si la tabla tenía esas columnas. Esto era
inofensivo mientras el único `Update` real venía de editar una capa con
geometría (todas tienen `updated_by`), pero al generalizar a
`plano_mensura`/`tierra` alguien editó directo la tabla intermedia
`plano_mensura_intervencion` (sin `updated_by`) y rompió con
`WFS Exception: No such property: updated_by`. Corregido agregando el mismo
chequeo para `Update`, vía el `Catalog` de GeoServer
(`GeoServerExtensions.bean("catalog")` -- **no** `bean(Catalog.class)`, que
tira `MultipleBeansException` porque el contexto tiene más de un bean de
tipo `Catalog`, el crudo y el envuelto con seguridad; se vio en vivo al
probar esto: con `bean(Catalog.class)` el chequeo fallaba silenciosamente
para TODAS las tablas, incluidas las que sí tienen `updated_by`, rompiendo
el plugin entero hasta corregirlo).

## Verificación manual rápida

Si algo falla y `verify` no alcanza para diagnosticar:

```bash
# ¿el servicio de roles django lee los roles de Django?
curl -u admin:$GEOSERVER_ADMIN_PASSWORD $GEOSERVER_URL/rest/security/roles/user/admin.json

# ¿la capa está publicada y responde?
curl -u admin:$GEOSERVER_ADMIN_PASSWORD "$GEOSERVER_URL/gdu/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=gdu:localidad&count=1"
```

## Pendiente de esta automatización (no bloquea el deploy, pero hay que
## decidirlo antes de ir más allá del piloto)

- **Quién puede escribir `localidad`**: usamos `GDU_ADMIN_USER` en
  `templates/layers.properties` como gate de escritura porque hoy ningún
  grupo de Django tiene `change_localidad`/`add_localidad`/`delete_localidad`
  (la edición nunca pasó por el modelo de permisos de Django). Si en algún
  momento se define un grupo específico para esto, es un cambio de una línea
  en `templates/layers.properties`.
- **LDAP en GeoServer**: validado a mano contra el AD real de producción
  (2026-09-09, con VPN activa hacia `10.106.16.3`) -- no está en
  `deploy_geoserver.sh` todavía. Se configuró un proveedor de autenticación
  `security/auth/ldap-ipduv/config.xml` (`<ldap>`, clase
  `org.geoserver.security.ldap.LDAPAuthenticationProvider`) replicando el
  mismo bind DN/base/filtro que ya usa Django
  (`GDU_LDAP_BIND_DN`/`GDU_LDAP_SEARCH_BASE`/`GDU_LDAP_SEARCH_FILTER` en
  `polizador/.env`): `serverURL=ldap://10.106.16.3:389/dc=ipduv,dc=gov,dc=ar`,
  `userFilter=(sAMAccountName={0})`, `user=IPDUV\admindeu` (cuenta de bind),
  agregado a `authProviderNames` junto al `default` existente. Los nombres de
  campo (`serverURL`, `userFilter`, `userNameAttribute`, `user`, `password`,
  `useTLS`, `bindBeforeGroupSearch`) salen del bytecode real de
  `gs-sec-ldap-2.26.2.jar` (`LDAPBaseSecurityServiceConfig`/
  `LDAPSecurityServiceConfig`), no adivinados. Deliberadamente NO se
  configuró ningún campo de búsqueda de grupos LDAP (`groupSearchBase` etc.)
  ni `userGroupServiceName` -- la autenticación (LDAP) y la autorización
  (roles) se mantienen desacopladas a propósito: LDAP solo valida
  usuario/contraseña, y el servicio de roles JDBC (`django`) sigue siendo
  quien resuelve los roles por username, sin cambios.

  Validado con la cuenta de bind (`admindeu`) contra un endpoint REST
  abierto: contraseña correcta -> 403 (autenticado, sin roles, porque
  `admindeu` no es un usuario de Django); contraseña incorrecta o usuario
  inexistente -> 401 (no autenticado) -- esa distinción solo es posible con
  un bind real contra el AD. No se probó con la contraseña real de un
  usuario de GDU (no corresponde pedirla), pero las dos mitades del
  mecanismo (bind LDAP; resolución de roles por username) ya estaban
  validadas por separado.

  Como con el servicio de roles, la contraseña de bind necesitó
  `configPasswordEncrypterName=plainTextPasswordEncoder` (ver más arriba) --
  se dejó así de forma permanente en el piloto, ya no se revierte a PBE.

  **Ya sumado a `deploy_geoserver.sh`** (`templates/ldap-auth-config.xml.tmpl`
  + variables `LDAP_BIND_DN`/`LDAP_BIND_PASSWORD`/`LDAP_SERVER_URL`/
  `LDAP_USER_FILTER`, ver "Variables de entorno" más arriba -- opcional, sin
  el bind DN/contraseña simplemente no se agrega el proveedor). El secreto
  real de `polizador/.env` no está hardcodeado en ningún archivo del repo.
  `phase_verify` repite la misma prueba 401-vs-403 si `LDAP_BIND_DN`/
  `LDAP_BIND_PASSWORD` están definidas. Al escribir el template se encontró
  y corrigió un bug real de bash (no de GeoServer): escribir el default de
  `LDAP_USER_FILTER` como `${LDAP_USER_FILTER:-(sAMAccountName={0})}`
  reordena caracteres -- las llaves de `{0}` dentro del valor default
  confunden el parseo de `${...}` (reproducido aislado). El script usa una
  asignación en dos pasos en su lugar.
- **Catalog Mode: `CHALLENGE`, no `HIDE` (decisión resuelta, spike N:N,
  2026-09-10)**: se había comprobado en la Fase 3 que con `mode=HIDE`, un
  `GetCapabilities`/`GetFeature` sin autenticar no devuelve error -- devuelve
  HTTP 400 "tipo desconocido", **sin header `WWW-Authenticate`** (verificado
  con `curl -i`), como si la capa no existiera. El cliente WFS de QGIS no
  tiene ningún 401 al cual reaccionar mostrando un diálogo de login, así que
  si el datasource no trae credenciales desde el arranque, la capa aparece
  como "no disponible" (con el botón "Explorar" deshabilitado -- QGIS ni
  siquiera sabe que ahí hay un login posible). Esto quedó pendiente de
  decidir en la Fase 3; al generalizar a más capas (spike N:N) volvió a
  aparecer -- esta vez con las 9 capas del paquete de prueba fallando todas
  a la vez en QGIS real, lo que forzó a resolverlo. Se probó cambiar a
  `mode=CHALLENGE`: GeoServer pasa a devolver 401 + `WWW-Authenticate: Basic
  realm="GeoServer Realm"` para lo mismo, que es justo la señal que QGIS (y
  cualquier cliente HTTP estándar) sabe interpretar para ofrecer el login.
  Efecto secundario aceptado: un anónimo ve el NOMBRE de las capas
  protegidas en `GetCapabilities` (no sus datos, eso lo sigue bloqueando la
  Data Access Rule igual que antes) -- `HIDE` ocultaba hasta la existencia
  de la capa, `CHALLENGE` ya no. Con esto, un proyecto QGIS sin
  `username`/`password` embebidos (el caso recomendado, ver
  `qgis-gdu/README.md`) ya puede pedir login interactivo por capa como
  cualquier WFS protegido estándar.
- **Crear un usuario de prueba en el store XML local**: los usuarios reales
  autentican vía LDAP, no contra `security/usergroup/default/users.xml` (que
  con la instalación nativa ya persiste entre restarts, ver "Bootstrap de la
  contraseña de admin" más arriba) -- pero si hace falta uno de prueba ahí,
  es más simple hacerlo por REST que por la UI: `POST
  /rest/security/usergroup/users` con
  `<user><userName>...</userName><password>...</password><enabled>true</enabled></user>`.
