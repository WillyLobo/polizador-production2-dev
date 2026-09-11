# Instalación de GeoServer en producción — runbook

Guía operativa paso a paso para levantar GeoServer/WFS-T en el servidor real
de IPDUV y generar el `.qgz` que cada usuario abre en QGIS. Es un resumen
accionable; el detalle y las decisiones de diseño (por qué `CHALLENGE` y no
`HIDE`, por qué el plugin Java, por qué contraseñas en texto plano en el data
dir, etc.) están en `geoserver/README.md` y `qgis-gdu/README.md` — este
documento no los repite, los referencia.

**Estado al escribir esto (2026-09-11):** todo lo de acá está validado contra
el equivalente local (`192.168.0.51`, donde Postgres y GeoServer corren en el
mismo host), no contra el servidor de producción real (todavía no
definido/alcanzado, y no necesariamente colocado con Postgres). Antes de usar
esto en producción, revisar la sección "Pendiente antes de ir a producción"
al final.

**Cambio de arquitectura (2026-09-11): ya no es un contenedor Docker.**
GeoServer ahora se instala como servicio **nativo** (distribución "bin"
oficial con Jetty embebido, un usuario de sistema `geoserver` dedicado, un
unit de systemd que el propio script escribe) — se abandonó Docker porque el
WAR de GeoServer 2.26.2 no es compatible con Tomcat 10 (el único que Ubuntu
empaqueta hoy; ver `geoserver/README.md` para el detalle técnico). Si este
runbook todavía menciona un contenedor en algún lado que no se haya
actualizado, es texto viejo — el comportamiento real es el que describe
`geoserver/README.md`.

## 0. Qué se instala

- GeoServer 2.26.2 como servicio **nativo** (no Docker), publicando por
  WFS-T las tablas de `catastro.*` que ya están validadas (`localidad`,
  `manzana`, `calle`, `vivienda_punto`, `intervencion`+sus relaciones N:N,
  `plano_mensura`+la suya — ver lista completa en `deploy_geoserver.sh` →
  `GS_FEATURETYPES`).
- Un servicio de roles JDBC que lee en vivo los `Group` de Django (por
  Postgres) — la autorización (qué puede editar cada usuario) sigue
  gobernada por Django, no por GeoServer.
- Opcionalmente, un proveedor de autenticación LDAP contra el mismo AD que ya
  usa Django (para que los usuarios reales logueen con su usuario de red, no
  con una cuenta local de GeoServer).
- Un plugin Java chico (`gdu-updated-by-listener.jar`) que completa
  `updated_by`/`updated_at` con el usuario autenticado real en cada
  Insert/Update WFS-T.

Todo esto lo automatiza `geoserver/deploy_geoserver.sh`. Lo que **no**
automatiza: la migración de la base de datos en sí (eso es un tema aparte,
ver "Pendiente"), y la generación del `.qgz` por usuario (paso 5 de este
documento).

## 1. Prerrequisitos

**Dónde corre cada fase (importante, cambió con el pase a nativo):**
- `postgres` (el paso de `CREATE ROLE`) usa `sudo -u postgres psql` por
  socket local (peer auth) -- **tiene que correrse en el propio servidor de
  Postgres de producción**, con sudo habilitado hacia el usuario del sistema
  operativo `postgres`. Confirmado que en producción, igual que en dev, el
  rol `postgres` no tiene contraseña seteada, así que no hace falta pedirla
  ni abrir `pg_hba.conf` a auth por TCP para un superusuario.
- `geoserver` **tiene que correrse en la máquina que va a alojar
  GeoServer** -- instala paquetes/usuario de sistema/unit de systemd
  localmente con `sudo`, no hay forma de que aprovisione una máquina remota.
  Si esa máquina es la MISMA que Postgres, `PGHOST=127.0.0.1` alcanza sin
  tocar nada más. Si es una máquina **distinta**, `PGHOST` tiene que ser la
  dirección real por la que esa máquina alcanza al Postgres de producción, y
  hay que confirmar que `pg_hba.conf` en el servidor de Postgres tenga (o se
  le agregue) una regla `host` que permita conexión TCP desde esa IP para
  `PG_APP_USER` y para el rol `geoserver_piloto` (el datastore) -- el script
  no gestiona `pg_hba.conf` por su cuenta.
- `verify` solo hace `curl` contra `GEOSERVER_URL`, así que puede correr
  desde cualquier máquina con red hacia GeoServer.

**Prerrequisitos concretos:**
- Sudo en la máquina de GeoServer para: crear el usuario de sistema
  `geoserver`, instalar en `/opt/geoserver` (o donde apunte
  `GEOSERVER_HOME`), y gestionar el unit de systemd.
- **Acceso a internet saliente hacia SourceForge** desde la máquina de
  GeoServer, al menos la primera vez (descarga
  `geoserver-2.26.2-bin.zip`, ~113MB) -- si el servidor de producción está
  restringido/sin salida a internet, hay que bajar ese zip por otro lado y
  adaptar `provision_geoserver_native()` para leerlo de un path local en vez
  de `curl`-earlo. SourceForge corta la conexión a mitad de descarga con
  cierta frecuencia; el script ya reintenta con resume (`curl -C -
  --retry`), pero si la máquina no tiene salida a internet directamente esto
  no alcanza.
- Un usuario de Postgres con privilegio para crear el schema
  `geoserver_auth` y hacer `GRANT` sobre `catastro.*` — el mismo `DBUSER`
  que usa Django (`polizador/.env`) alcanza.
- La base de datos de producción ya tiene que tener corrida la migración de
  Django `polizador/gdu/migrations/0003_calle_ejecutor_inspector_...` (crea
  las tablas `ejecutor`/`inspector`/`intervencion_ejecutor`/etc. que
  `02_provision_schema.sql` va a hacer `GRANT` sobre ellas — si esa migración
  no corrió, la fase `postgres` va a fallar con "relation ... does not
  exist").
- Si se va a habilitar LDAP: las mismas credenciales de bind que ya usa
  Django (`GDU_LDAP_BIND_DN`/`GDU_LDAP_BIND_CREDENTIALS` en
  `polizador/.env`) y conectividad hacia `10.106.16.3:389`.
- `curl`/`psql`/`unzip` disponibles en la máquina de GeoServer (`unzip` se
  auto-instala vía `apt` si falta); `psql` además en la máquina de Postgres
  para la fase `postgres`.

## 2. Variables de entorno

Ver la tabla completa en `geoserver/README.md` → "Variables de entorno". En
producción, como mínimo (esto también se puede poner en un `geoserver/.env`
en vez de hacer `export` a mano en cada sesión de shell -- `deploy_geoserver.sh`
lo sourcea solo si existe; no se versiona, ver `geoserver/.gitignore`):

```bash
# GeoServer (servicio nativo, no Docker)
export GEOSERVER_ADMIN_PASSWORD='<contraseña nueva, no la del piloto>'
export GEOSERVER_DATA_DIR=/opt/geoserver_data         # o la ruta real en el servidor de producción
export GEOSERVER_URL=http://127.0.0.1:8080/geoserver  # la fase geoserver corre local a su propia máquina, ver sección 1 -- casi siempre 127.0.0.1

# Postgres de producción -- correr la fase "postgres" EN este servidor (ver sección 1)
export PGHOST='127.0.0.1'   # o la IP real si la fase "geoserver" corre en OTRA máquina, ver sección 1
export PGDATABASE='<nombre de la base de producción>'
export PG_APP_USER='<DBUSER de polizador/.env>' PG_APP_PASSWORD='<DBPASSWORD de polizador/.env>'
export GEOSERVER_DS_PASSWORD='<contraseña nueva para geoserver_piloto>'
export GEOSERVER_SECURITY_DB_PASSWORD='<contraseña nueva para geoserver_security>'

# LDAP (opcional pero recomendado en producción -- sin esto, solo el admin local puede loguear)
export LDAP_BIND_DN='IPDUV\admindeu'                  # mismo valor que GDU_LDAP_BIND_DN
export LDAP_BIND_PASSWORD='<mismo valor que GDU_LDAP_BIND_CREDENTIALS>'
```

**Ya no hace falta `PG_SUPERUSER`/`PG_SUPERUSER_PASSWORD`** -- el paso de
`CREATE ROLE` usa `sudo -u postgres` local (ver sección 1), sin necesitar
una contraseña de superusuario.

**Importante — contraseñas nuevas, no las del piloto**: `GEOSERVER_DS_PASSWORD`,
`GEOSERVER_SECURITY_DB_PASSWORD` y `GEOSERVER_ADMIN_PASSWORD` del piloto están
en texto plano en este historial de trabajo y en el data dir del piloto — no
reusarlas en producción.

## 3. Deploy

Desde `geoserver/`, con las variables de arriba exportadas:

```bash
./deploy_geoserver.sh postgres     # crea roles + schema geoserver_auth + GRANTs en catastro.* -- correr en el server de Postgres
./deploy_geoserver.sh geoserver    # instala/actualiza GeoServer nativo + workspace/datastore/capas + seguridad + plugin -- correr en el server de GeoServer
./deploy_geoserver.sh verify       # repite la batería de pruebas allow/deny sobre TODAS las capas de GS_FEATURETYPES
```

(`./deploy_geoserver.sh all` corre las tres en la misma máquina -- solo
tiene sentido si esa máquina es a la vez el servidor de Postgres y el que va
a alojar GeoServer, ver sección 1.)

`verify` tiene que terminar con `Verificación completa OK`. Si algo falla, el
mensaje de `die` indica qué chequeo fue — ver "Verificación manual rápida" en
`geoserver/README.md` para diagnosticar a mano con `curl`.

Es re-ejecutable: correr `geoserver` de nuevo (por ejemplo tras sumar una
capa a `GS_FEATURETYPES`, o para redeployar el plugin jar tras recompilarlo)
no rompe lo que ya está publicado.

## 4. Configuración extra que el script NO cubre

Nada de esto bloquea el deploy en sí, pero hay que decidirlo/hacerlo antes de
dar por terminada la puesta en producción:

1. **LDAP**: si se exportaron `LDAP_BIND_DN`/`LDAP_BIND_PASSWORD`, ya queda
   configurado por el script. Si no, los usuarios reales no van a poder
   loguear en GeoServer con su usuario de red — solo funciona el `admin`
   local. Validar con `verify` (corre el chequeo 401-vs-403 automáticamente
   si esas dos variables están definidas).
2. **Roles Django de lectura por capa**: hoy `templates/layers.properties`
   usa `GDU_ADMIN_USER` como gate de **escritura** en todas las capas (nadie
   tiene `change_<tabla>` en Django todavía — es una decisión pendiente, ver
   `geoserver/README.md` → "Pendiente"), y para varias capas también como
   gate de **lectura** (`intervencion`, `ejecutor`, `plano_mensura`, etc. —
   ver la lista completa en el archivo). Antes de dar acceso real a usuarios
   que no sean admin, confirmar que el grupo de Django que corresponda
   (`GDU_ADMIN_USER`, `LOCALIDADES_TODOS_LOS_USUARIOS`,
   `GDU_CATASTRO_URBANO_VER`, `GDU_VIVIENDAS_VER`, ...) exista de verdad en
   `Group` y tenga a los usuarios correctos — el servicio de roles JDBC solo
   traduce nombres de grupo Django a roles GeoServer 1:1 (mayúsculas, `_` en
   vez de espacios/símbolos, ver `geoserver_auth.roles` en
   `sql/02_provision_schema.sql`), no crea nada por su cuenta.
3. **El trigger `catastro.set_updated()` con `COALESCE`**: `02_provision_schema.sql`
   lo reemplaza (`CREATE OR REPLACE FUNCTION`) como parte de la fase
   `postgres` — no hace falta nada manual, pero es un cambio que afecta a
   las ~30 tablas de `catastro` que comparten ese trigger (no solo las
   publicadas por WFS-T). Confirmar que no hay otro trigger o migración de
   Django que lo pise después.
4. **El plugin jar se reinstala en cada corrida de `geoserver`**, no vive en
   el data dir persistente (`WEB-INF/lib` se borra y recrea si se
   redespliega GeoServer por un cambio de `GEOSERVER_VERSION`) — si en algún
   momento se reinstala GeoServer desde cero SIN pasar por
   `deploy_geoserver.sh geoserver`, `updated_by` deja de completarse con el
   usuario real (el trigger cae a `current_user` = `geoserver_piloto` para
   todos, sin romper nada, pero sin distinguir usuarios). Siempre
   reinstalar/actualizar vía el script, no a mano.
5. **Filesystem del data dir**: la política de contraseñas de configuración
   quedó en texto plano (`plainTextPasswordEncoder`, decisión documentada en
   `geoserver/README.md`) — restringir el acceso de lectura a
   `GEOSERVER_DATA_DIR` al usuario de sistema `geoserver` en el servidor de
   producción.
6. **Backups**: `GEOSERVER_DATA_DIR` (config de GeoServer: workspace,
   datastore, reglas de seguridad) no tiene datos de catastro en sí (esos
   viven en Postgres, con su propio backup) pero si se pierde hay que
   rehacer el deploy desde cero — no crítico, pero conviene que quede en el
   mismo esquema de backup del servidor que el resto de la config.
7. **Primer login de admin**: en un data dir nuevo, GeoServer genera una
   contraseña de admin aleatoria que nunca se revela en texto plano --
   `deploy_geoserver.sh geoserver` la rota sola a `GEOSERVER_ADMIN_PASSWORD`
   la primera vez (ver "Bootstrap de la contraseña de admin" en
   `geoserver/README.md`), usando un login temporal con la master password
   generada. No requiere ninguna acción manual, pero si `geoserver` falla
   justo en ese paso, el mensaje de error indica dónde mirar
   (`security/masterpw.info` y `security/masterpw/default/config.xml` en el
   data dir).

## 5. Verificación manual post-deploy

Además de `./deploy_geoserver.sh verify`:

```bash
# ¿el servicio de roles resuelve un usuario real de Django?
curl -u admin:$GEOSERVER_ADMIN_PASSWORD "$GEOSERVER_URL/rest/security/roles/user/<username>.json"

# ¿una capa protegida responde 401 (no 400) a un anónimo?
curl -i "$GEOSERVER_URL/gdu/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=gdu:localidad&count=1"
```

## 6. Generar el `.qgz` para un usuario (ej. `mazzario`)

El proyecto QGIS real (`gdu.qgz`, o el que use ese usuario) tiene ~180 capas;
solo las listadas en `GS_FEATURETYPES` (arriba) están publicadas por WFS-T.
`scripts/reconectar_wfs.py` reescribe **solo esas**, dejando el resto del
proyecto intacto (apuntando a Postgres directo, como siempre) — es el
`.qgz` completo para uso real, a diferencia del paquete recortado
(`--solo-esta-capa`) que se usó para probar en este ciclo de trabajo.

### 6.1. Confirmar qué capas existen en el `.qgz` de ese usuario

No todos los `.qgz` en circulación tienen las mismas capas armadas (ver
`tierra`, que no existe en ninguno de los `.qgz` disponibles al momento de
escribir esto — si el de `mazzario` sí la tiene, se puede sumar a la lista;
si no, se omite sin problema, `tierra` ya queda publicada en GeoServer de
todos modos). Si no se sabe de antemano, simplemente correr el script con la
lista completa de `GS_FEATURETYPES` — si alguna capa no existe en ese
`.qgz`, el script corta con un error claro (`se esperaba exactamente un
<id>...</id>`) señalando cuál, y se la saca de `--layers` y se reintenta.

### 6.2. Correr el script

Desde `qgis-gdu/` (o donde esté el `.qgz` real de ese usuario — copiarlo ahí,
junto con su carpeta `forms/`, si viene de otro lado):

```bash
python3 scripts/reconectar_wfs.py \
  --input gdu.qgz \
  --output gdu.wfs.mazzario.qgz \
  --geoserver-url http://<host-geoserver-produccion>:8080/geoserver \
  --layers localidad manzana calle vivienda_punto \
           intervencion inspector ejecutor intervencion_inspector intervencion_ejecutor \
           plano_mensura plano_mensura_intervencion \
  --force
```

**Sin `--username`/`--password`** a propósito: en producción no hay que
embeber credenciales en el `.qgz` — QGIS va a pedir usuario/contraseña la
primera vez que abra cada capa (con `CHALLENGE` activo, ver
`geoserver/README.md`), y esas credenciales deberían ser las mismas
LDAP/AD de red del usuario, no una cuenta compartida. **Ojo**: así como está
el comando de arriba, tablas grandes (~1200-2000 filas) van a andar muy
lentas o crashear QGIS — ver la advertencia de rendimiento y la dirección
decidida (`--authcfg`) en la sección "Pendiente" más abajo antes de repartir
esto a un usuario real con tablas de ese tamaño.

No usar `--solo-esta-capa` para un `.qgz` de uso real — esa opción existe
solo para recortar el proyecto a un puñado de capas al probar sin acceso al
resto de la infraestructura (ver `qgis-gdu/README.md`); un usuario real
necesita el proyecto completo, con el resto de las ~180 capas intactas.

### 6.3. Entregar el `.qgz`

- `gdu.wfs.mazzario.qgz` **más** la carpeta `forms/` completa, con la misma
  disposición relativa (`forms/` al lado del `.qgz`) — si no, QGIS tira
  `NameError: name 'my_form_open' is not defined` al abrir cualquier
  formulario custom (la capa carga igual, pero el form no). Ver
  "Importante para distribuir el `.qgz` a otra máquina" en
  `qgis-gdu/README.md`.
- El usuario necesita, en Django, pertenecer a los grupos que dan lectura a
  las capas que va a usar (ver punto 2 de la sección 4) y, si va a editar,
  al grupo `GDU_ADMIN_USER` (hoy el único con permiso de escritura — no hay
  todavía un rol de edición más granular, ver "Pendiente" en
  `geoserver/README.md`).
- Confirmar que ese usuario resuelve bien sus roles antes de mandarle el
  archivo: `curl -u admin:$GEOSERVER_ADMIN_PASSWORD "$GEOSERVER_URL/rest/security/roles/user/<username>.json"`.

## Pendiente antes de ir a producción

Estos puntos están identificados pero **no resueltos** — no bloquean un
deploy de prueba, pero sí una puesta en producción real con usuarios finales:

- **Rendimiento de QGIS sin credenciales embebidas**: se comprobó en el
  piloto que `mode=CHALLENGE` sin credenciales embebidas duplica los
  round-trips por página en tablas de ~1200-2000 filas (401 + reintento por
  cada página), causando esperas de varios minutos y hasta un crash de QGIS
  en Windows. Para el paquete de prueba se resolvió embebiendo credenciales
  (aceptable solo porque no se distribuye más allá del spike) — para
  producción, con credenciales reales por usuario, esto sigue sin resolverse.

  **Dirección decidida (2026-09-11), pendiente de validar en QGIS real**:
  usar el Auth Manager de QGIS en vez de `username`/`password` embebidos.
  `reconectar_wfs.py` ya soporta `--authcfg <id>` (mutuamente excluyente con
  `--username`/`--password`): escribe `authcfg='<id>'` en el datasource de
  cada capa en vez de credenciales sueltas. Ese id de 7 caracteres NO es un
  secreto — referencia una config "Basic" que cada usuario carga **una sola
  vez, en su propia máquina** (Settings > Options > Authentication en QGIS,
  requiere haber seteado antes una master password para `qgis-auth.db` si
  es la primera vez que usa el Auth Manager), con sus propias credenciales
  LDAP/AD reales. A diferencia de dejar `username`/`password` vacíos (que
  depende del diálogo de login de Qt sobre un 401 real, sin cachear entre
  páginas), `authcfg` hace que QGIS mande el header `Authorization` desde la
  primera request de cada página — mismo comportamiento rápido que embeber
  la contraseña, sin dejar ningún secreto real en el `.qgz`.

  Punto abierto para la validación: el id de la config "Basic" lo asigna
  QGIS al crearla (no hay forma confirmada de fijarlo de antemano por
  script), así que el orden de trabajo por usuario queda invertido respecto
  al flujo actual de la sección 6: primero crear/confirmar la config en la
  máquina del usuario (o leer el id si ya la tiene cargada de una entrega
  anterior), recién después correr `reconectar_wfs.py --authcfg <ese-id>`
  para generar SU `.qgz` — coordinación extra por usuario, pero compatible
  con el hecho de que ya se genera un `.qgz` nombrado por usuario (ej.
  `gdu.wfs.mazzario.qgz`), no un archivo único para todos. Falta probar de
  punta a punta contra una tabla de ~1200-2000 filas para confirmar que
  realmente colapsa los round-trips como se espera.
- **`tierra`**: publicada y verificada del lado de GeoServer, pero sin
  ningún `.qgz` disponible con esa capa armada — no se puede repartir hasta
  que exista un proyecto QGIS real con "Tierra" como capa propia.
- **Migración de la base real** (`db_gdu`@10.106.16.118 u otra fuente de
  producción hacia la base que va a usar este GeoServer): fuera de alcance
  de este documento y del script — es una decisión operativa aparte.
- **QGIS 3.10 vs 3.44**: el circuito completo se validó en QGIS 3.44
  ("Solothurn"); las estaciones de IPDUV corren 3.10 ("A Coruña") — falta
  confirmar el mismo checklist contra esa versión exacta antes de repartir
  `.qgz` de producción a esas estaciones.
- **Rol de escritura único (`GDU_ADMIN_USER`)**: ningún grupo de Django
  tiene hoy `change_<tabla>` para ninguna de estas capas — todos los
  editores reales van a necesitar `GDU_ADMIN_USER` hasta que se defina un
  rol más granular.
