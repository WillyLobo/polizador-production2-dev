# qgis-gdu — piloto WFS-T (Fase 3 + 4a)

Copia de trabajo de `env/.snipets/gdu/` (que sigue siendo la referencia,
sin tocar) para probar la Fase 3 del plan: reconectar capas del proyecto a
WFS-T vía GeoServer y validar que el plugin QGIS existente (`forms/nn.py`,
`forms/layer_config.py`, los `.ui`) sigue funcionando sin cambios.

`gdu.qgz` y `forms/` son copia exacta del original (`nn.py`/`layer_config.py`
byte a byte idénticos) — el resto de las capas del proyecto siguen apuntando
a Postgres directo, sin tocar, a propósito. Piloto (Fase 3): `localidad`.
Fase 4a suma `manzana`/`calle`/`vivienda_punto` (mismo mecanismo, capas
elegidas por cubrir Polygon/LineString/Point que `localidad` no probaba).
`intervencion`/`tierra` (con relaciones N:N) quedan afuera a propósito hasta
validar aparte si ese patrón de guardado funciona contra WFS-T.

**Importante para distribuir el `.qgz` a otra máquina**: el formulario custom
de cada capa se referencia con ruta relativa (`./forms/localidad.ui`,
`./forms/nn.py` -- se ve en el XML del proyecto como
`editforminitfilepath`/`editforminitcodesource=1`), resuelta relativa a la
carpeta donde esté el `.qgz`. Si se copia el `.qgz` solo, sin `forms/` al
lado, QGIS no encuentra el código y tira `NameError: name 'my_form_open' is
not defined` al abrir el formulario (aunque la capa cargue bien) -- hay que
llevar siempre el `.qgz` junto con `forms/`, con esa misma estructura relativa.

## 1. Generar el proyecto reconectado

```bash
python3 scripts/reconectar_wfs.py --geoserver-url http://<host-geoserver>:8080/geoserver \
  --layers localidad manzana calle vivienda_punto --force
```

`--layers` es opcional (default: `localidad` sola, para compatibilidad con
la Fase 3) y acepta una o más capas separadas por espacio.

Para este ciclo de piloto, el GeoServer corre en el mismo host que este repo
(contenedor Docker en modo `--network host`, sin firewall de por medio) y ya
es alcanzable desde cualquier máquina de la LAN en `192.168.0.51:8080` sin
tocar nada del lado del servidor. `gdu.wfs.qgz` en este directorio ya está
generado con esa URL, listo para abrir en QGIS.

Esto escribe `gdu.wfs.qgz` (ignorado por git — se regenera, no se versiona,
porque embebe la URL de GeoServer de un entorno puntual). Por cada capa
pedida solo toca 3 líneas del proyecto: el `<datasource>`/`<provider>` de esa
capa y su entrada en el panel de capas (`<layer-tree-layer>`) — todo lo demás
queda byte a byte igual al original (verificado con diff al escribir el
script para el caso de una sola capa).

Sin `--username`/`--password`, QGIS va a pedir credenciales la primera vez
que intente cargar la capa (recomendado, para no dejar contraseñas dentro del
`.qgz`). Para probar el circuito completo de lectura+escritura hace falta una
identidad con rol `GDU_ADMIN_USER` o `ADMIN` en GeoServer (ver
`geoserver/README.md` — hoy ningún grupo de Django tiene permiso de edición
sobre `localidad` todavía, así que el único usuario realmente probado con
escritura es el `admin` de GeoServer).

### Copia liviana (solo las capas pedidas, sin el resto del proyecto)

El proyecto completo sigue teniendo el resto de las capas apuntando al
Postgres real de producción (`10.106.16.118`) sin tocar, a propósito -- pero
eso significa que QGIS va a intentar conectarse a todas esas capas al abrir
el proyecto, y si ese host no es alcanzable desde donde se prueba (lo normal
fuera de la red de IPDUV), tira un diálogo de credenciales por cada una.

Para evitarlo al probar, `--solo-esta-capa` genera una copia que elimina todo
lo que no esté en `--layers` **ni sea una dependencia de esas capas**
(maplayer, entrada del panel de capas, leyenda, orden de capas/custom-order,
relaciones, layouts de impresión):

```bash
python3 scripts/reconectar_wfs.py --geoserver-url http://192.168.0.51:8080/geoserver \
  --layers localidad manzana calle vivienda_punto \
  --output gdu.wfs.solo-piloto.qgz --solo-esta-capa --force
```

**Capas de soporte (dependencias vía widget de relación):** varias capas
tienen un campo con un combo "RelationReference" que apunta a otra capa (ej.
`manzana`/`calle`/`vivienda_punto` tienen un campo `id_intervencion` que
depende de la capa `Intervención`; `vivienda_punto` también depende de
`Resolución de Costos` vía `res_costos`). Si esa capa dependiente no está en
el proyecto, QGIS tira "Falta dependencia de formulario de capa" al abrir la
capa que la necesita (así se detectó este caso: `--solo-esta-capa` recortaba
esas dependencias por error). El script calcula el cierre transitivo de estas
dependencias automáticamente y, para las que no estén en `--layers`, las
conserva conectadas directo a Postgres (`--pg-host`/`--pg-port`/`--pg-dbname`/
`--pg-schema`, default: el mismo Postgres del piloto, schema `catastro`) en
vez de eliminarlas o pasarlas a WFS -- son de solo lectura en la práctica, no
se editan en este piloto. QGIS va a pedir credenciales de Postgres (no de
GeoServer) la primera vez que las cargue.

Es una conveniencia solo para probar -- `gdu.qgz` (la copia de referencia) y
`gdu.wfs.qgz` (la reconexión "completa", con las otras capas intactas) no se
tocan.

## 2. Validar contra QGIS real (manual — no tiene sustituto automatizado)

**Validado — 2026-09-09.** Esto era lo único que este agente no podía hacer
por su cuenta (no hay QGIS instalado en este entorno). Se probó contra QGIS
Desktop **3.44.14 "Solothurn"** (no 3.10 "A Coruña", que es la versión
confirmada en las estaciones de IPDUV -- esta corrida fue en una máquina de
prueba con una versión más nueva; sigue siendo una validación real de que el
mecanismo funciona, pero falta confirmarlo también contra la versión exacta
de producción antes de dar la Fase 3 por cerrada del todo en ese sentido):

- [x] La capa "Localidades" carga y muestra los puntos (91 localidades en el
      piloto). Si QGIS pide credenciales, ahí es donde se prueba que el rol
      de lectura (`LOCALIDADES_TODOS_LOS_USUARIOS`/`ADMIN`) funciona.
- [x] "Alternar edición" está habilitado para esa capa (a diferencia del
      enfoque viejo, acá lo decide el proveedor WFS de QGIS negociando con
      GeoServer, no un GRANT de Postgres).
- [x] Doble click en un punto abre el formulario custom (`localidad.ui`,
      tamaño de ventana e inicialización via `my_form_open` de `nn.py`) igual
      que contra Postgres directo — confirma que no hizo falta tocar el
      plugin. (Ojo: esto requiere llevar `forms/` junto al `.qgz`, con la
      misma estructura relativa -- ver más abajo, "Importante para
      distribuir".)
- [x] Editar un registro existente y guardar: el cambio llega a
      `catastro.localidad` en Postgres (verificado con `SELECT` directo --
      se probó renombrando "Barranqueras" a "Barranquerasas").
- [x] Crear un registro nuevo (con geometría) y guardar: aparece en Postgres
      (se probó con un punto "Willyburg", apareció con id autogenerado).
- [x] Borrar un registro: desaparece de Postgres (se borró el mismo
      "Willyburg" de prueba).
- [x] Con una identidad que solo tenga el rol de lectura (`test_localidad_viewer`
      del piloto), la capa se muestra de solo lectura -- confirma que la
      Data Access Rule de escritura (`gdu.localidad.w`) se respeta también
      desde QGIS, no solo desde `curl`.

Con esto, la apuesta central del plan queda confirmada: el plugin QGIS
existente (`nn.py`/`layer_config.py`/los `.ui`) funciona sin ningún cambio
contra una capa respaldada por WFS-T en vez de Postgres directo, y los
permisos ahora los decide GeoServer (vía los roles sincronizados desde
Django) en vez de un GRANT de Postgres. Antes de generalizar a más capas
(Fase 4), falta: confirmar contra QGIS 3.10 exacto (se validó contra 3.44),
y las decisiones ya documentadas en `geoserver/README.md` (`updated_by` por
fila, quién puede editar cada capa, LDAP, `HIDE` vs `CHALLENGE`).

### Fase 4a — `manzana`/`calle`/`vivienda_punto`

**Validado — 2026-09-10.** Mismo checklist que Fase 3 (carga, alternar
edición, formulario custom, editar/crear/borrar con geometría) repetido
sobre las tres capas nuevas usando el paquete liviano
(`--solo-esta-capa`) -- confirma que el mecanismo no era casualidad de
`localidad`: funciona igual para Polygon (`manzana`), LineString (`calle`)
y un segundo caso de Point (`vivienda_punto`).

**Hallazgo:** abrir el formulario propio de `Intervención` (o
`Resolución de Costos`) dentro de este paquete tira
`KeyError: 'plano_mensura_intervencion_...'`. No es un bug de
`reconectar_wfs.py` -- `intervencion`/`tierra` están en el paquete solo
como capas de soporte de solo lectura (para el combo `RelationReference`
de `id_intervencion`/`res_costos`), y su propio formulario depende además
de las tablas intermedias N:N (`plano_mensura_intervencion`,
`intervencion_inspector`, `intervencion_ejecutor`, y sus tablas finales)
referenciadas por id de capa fijo en `layer_config.py`/`nn.py`, no por el
widget `RelationReference` que el script rastrea -- por eso el cálculo de
dependencias no las incluye. Confirma lo que el plan ya dejaba afuera de
este ciclo a propósito: el patrón de guardado N:N de `intervencion`/`tierra`
necesita un spike aparte. Mientras tanto, en este paquete de prueba no hay
que abrir el formulario propio de esas dos capas -- solo usarlas desde el
combo dentro de Manzana/Calle/Vivienda Puntual.

### Spike N:N — Intervención (inspectores/ejecutores)

**Validado — 2026-09-10.** Ver el plan `en-lugar-de-geoserver-hashed-cupcake.md`
para el contexto completo del riesgo que este spike probaba: `nn.py` guarda
las listas N:N del formulario de Intervención (`Planos`, `Inspectores`,
`Ejecutores`) con `layerNN.dataProvider().deleteFeatures()`/`addFeatures()`
llamado directo sobre el provider, **sin pasar por `layer.commitChanges()`**
-- no estaba probado si eso dispara una transacción WFS-T real contra un
layer WFS (a diferencia de Postgres directo, donde el provider no
bufferea). **Respuesta: sí funciona**, confirmado agregando/quitando
inspectores y ejecutores en una Intervención real y verificando con
`SELECT` directo en Postgres (`updated_by` correcto también).

Se publicaron y cablearon `intervencion`/`inspector`/`ejecutor`/
`intervencion_inspector`/`intervencion_ejecutor` (2 de las 3 relaciones N:N
de Intervención -- deliberadamente sin `plano_mensura`/
`plano_mensura_intervencion`, que tienen un riesgo aparte: un tipo enum
custom de Postgres en la tabla intermedia, mejor no mezclarlo con esta
prueba). **Desvío temporal**: en `forms/layer_config.py` (esta copia de
prueba, NO `env/.snipets/gdu/forms/`) la entrada `plano_mensura_intervencion`
de `LayerConfig.config['intervencion']['nn']` quedó comentada -- si no,
`nnForm.__init__` revienta con `KeyError` al buscar esa capa (que a
propósito no está en este paquete). Revertir cuando se aborde esa relación.

**Bug real encontrado y corregido, específico de WFS (`forms/nn.py`), en
DOS lugares:** el código usaba `feature.id()` (el `QgsFeatureId` interno de
QGIS) como si fuera el valor real de la columna `id`, y `layer.getFeature(
id_real)` como si `getFeature` buscara por ese valor en vez de por FID.
Contra Postgres directo el FID y el `id` real siempre coinciden, así que
nunca se había notado; contra WFS no necesariamente:

1. Del lado de la lista (Ejecutor/Inspector, `layerN`): pedir un ejecutor
   por su `id` real devolvía siempre el registro con el `id` inmediatamente
   anterior (ej. pedir "DELIEL" guardaba "DAL CONSTRUCCIONES", el vecino).
2. Del lado de Intervención misma (`self.feature`, la capa referenciante):
   un guardado terminaba en OTRA Intervención completamente distinta (ej.
   pedir guardar en el id 1001 terminaba guardando en el id 890) -- mismo
   bug, pero acá el desfasaje entre FID e `id` real no es un simple "-1",
   así que el síntoma parecía confusión de navegación al principio.

Corregido en esta copia de prueba con `buscar_feature_por_id()` (busca en
`layerN` por el atributo `"id"` real, no por FID) y `id_real()` (lee el
atributo `"id"` de `self.feature` de forma segura, sin asumir que exista)
en los lugares donde aplicaba. **Si se promueve este patrón de N:N a la
referencia real (`env/.snipets/gdu/forms/nn.py`), hay que portar este fix.**

**Tercer bug, preexistente (no específico de WFS, pero lo expuso este
ciclo):** el botón "Agregar" de cada lista NN solo se habilitaba/
deshabilitaba una vez, cuando se armaba el formulario de esa fila -- si
activabas "Alternar edición" DESPUÉS de pararte en esa fila, el botón
quedaba deshabilitado hasta ir a otra fila y volver. Corregido conectando
el estado del botón a las señales `editingStarted`/`editingStopped` de la
capa, así reacciona en vivo sin tener que navegar.

**Cuarto hallazgo:** al recién abrir la tabla de atributos de Intervención,
QGIS arma el primer formulario con un feature "parcial" que todavía no
tiene el campo `id` resuelto -- `feature.attribute('id')` tira `KeyError`
en vez de devolver `None`, lo que crasheaba QGIS. `id_real()` lo trata como
"sin id todavía" (deshabilita el botón, no crashea) en vez de romper.

Otros hallazgos de esta ronda (detalle completo en el plan):
Catalog Mode pasó de `HIDE` a `CHALLENGE` (permanente, `HIDE` no manda 401
así que QGIS no puede ofrecer el login); el cálculo de dependencias de
`reconectar_wfs.py` se generalizó para leer directo la sección `<relations>`
del proyecto en vez de perseguir cada estilo de widget por separado (había
3 estilos distintos, uno de ellos -- el campo "Res. Adjudicación" -- sin
ninguna config detectable en el `.qgs`); y con credenciales sin embeber +
`CHALLENGE`, las tablas de ~1200-2000 filas se volvieron muy lentas para
QGIS (min. de espera, un crash en Windows) -- se probó embebiendo
`--username`/`--password` en el `.qgz` de prueba y mejoró notablemente
(aceptable para un test que no se reparte más; para producción falta
revisar el patrón de autenticación real).

Checklist confirmado en QGIS real (registro existente de Intervención, el
botón "Agregar" de cada lista NN está deshabilitado para un feature nuevo
sin guardar):

- [x] El formulario de Intervención abre sin `KeyError` (con las listas de
      Inspectores y Ejecutores, sin la de Planos).
- [x] Agregar un inspector y un ejecutor a las listas, guardar el feature
      -- y que sea el registro correcto el que se agregó (no el vecino).
- [x] Confirmado en Postgres (`SELECT` directo sobre
      `catastro.intervencion_inspector`/`catastro.intervencion_ejecutor`).
- [x] `updated_by` en las filas nuevas de `intervencion_ejecutor` (tiene esa
      columna) refleja el usuario real autenticado, no `geoserver_piloto`.
- [x] Quitar elementos de una lista (todos los ejecutores menos uno, y el
      único inspector), guardar, confirmado en Postgres que desaparecieron
      -- `deleteFeatures()` también funciona contra WFS-T.

Con esto el spike queda cerrado: el patrón de guardado N:N (agregar y
quitar) funciona de punta a punta contra WFS-T.

### Generalización — `plano_mensura`/`tierra` (2026-09-10)

**`plano_mensura`/`plano_mensura_intervencion`: validado de punta a punta
en QGIS real.** Publicadas, verificadas (incluido un `Insert` manual por
`curl` confirmando que el enum `tipo_plano_mensura` se expone y escribe
como texto plano sin problema) y cableadas al paquete de prueba.
Descomentada la entrada `plano_mensura_intervencion` en
`forms/layer_config.py` (el desvío temporal del spike ya no aplica).
Checklist confirmado en QGIS real:

- [x] "Plano de Mensura" como capa normal (Polygon): edita geometría
      (plano 01-1-11), crea (id 2171, verificado `updated_by=admin`) y
      borra (mismo id, confirmado que desapareció de Postgres).
- [x] Intervención: la lista "Planos" ya no tira `KeyError`; agregar,
      editar (cambiar el plano vinculado) y quitar un plano funcionan.
- [x] **Bug encontrado y corregido en el camino**: editar
      `plano_mensura_intervencion` (sin `updated_by`) directo como capa
      propia (no vía `nn.py`) rompía con `WFS Exception: No such property:
      updated_by` -- era la "deuda menor" del plugin Java
      (`setOrReplaceProperty`) que el spike había dejado anotada sin
      tocar. Corregido en `geoserver/plugin/` -- ver
      `geoserver/README.md` para el detalle (incluye una vuelta de tuerca
      real: `GeoServerExtensions.bean(Catalog.class)` tira
      `MultipleBeansException`, hay que pedirlo por nombre).

**`tierra`: bloqueada, no por WFS.** Se probó por `curl` que las 6 columnas
enum custom de `tierra` (`tipo`, `tipo_oferente`, `tipo_inscripcion`,
`localizacion`, `superficie`, `estado`) también se escriben bien vía
WFS-T -- ese riesgo está resuelto. Pero **no existe una capa "Tierra" en
ningún `.qgz` disponible**: se revisaron `gdu.qgz` (este repo) y
`env/.snipets/gdu/Tierras/gdu.qgz` (69 capas, ninguna es Tierra); el id que
`forms/layer_config.py` espera (`tierra_d651e31d_ddd2_4ad6_a544_20308cb56acc`)
no aparece en ningún `<maplayer>` de ninguno de los dos. Solo existe la
tabla intermedia `plano_mensura_tierra`, huérfana (referencia a una capa
que no está cargada en ningún proyecto disponible). `tierra`/
`plano_mensura_tierra` quedaron publicadas y verificadas del lado de
GeoServer de todos modos (no hace daño tenerlo listo), pero sin un `.qgz`
real con la capa Tierra armada no hay nada que probar del lado de QGIS.
El usuario decidió dejarla afuera por ahora -- retomar si aparece un
proyecto con esa capa.

### Fixes de `nn.py` portados a la referencia real (2026-09-10)

Los 4 fixes encontrados en `forms/nn.py` durante el spike/generalización
(`buscar_feature_por_id`/`id_real()` en vez de `feature.id()`/
`layer.getFeature()`, y el botón "Agregar" reaccionando en vivo a
`editingStarted`/`editingStopped`) se portaron a
**`env/.snipets/gdu/forms/nn.py`** (la referencia real, hasta ahora
intacta) -- ya no son un desvío temporal de esta copia de prueba, son la
implementación real. Verificado con `diff`: el código funcional de ambos
archivos es idéntico, solo cambia la redacción de los comentarios/
docstrings (ya no hablan de "spike temporal"). Todos los fixes son
compatibles con Postgres directo también (no solo WFS): contra Postgres,
FID y el atributo `id` siempre coinciden, así que el comportamiento no
cambia para el uso actual en producción.

## Archivos

- `gdu.qgz` — copia sin modificar del proyecto de referencia.
- `forms/` — copia de `layer_config.py`, `nn.py` y los `.ui`. Ya no es una
  copia byte a byte de `env/.snipets/gdu/forms/` (que sigue siendo la
  referencia real) -- son funcionalmente idénticas (los fixes de `nn.py`
  del spike se portaron a la referencia, ver arriba), pero difieren en
  comentarios/docstrings.
- `scripts/reconectar_wfs.py` — genera `gdu.wfs.qgz` (todas las capas del
  proyecto, solo las de `--layers` reconectadas) o, con `--solo-esta-capa`,
  una copia liviana con únicamente esas capas (recomendado para probar).
