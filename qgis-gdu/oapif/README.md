# Proyecto QGIS de GDU sobre OGC API - Features

`gdu-oapif.qgz` reemplaza al `gdu.qgz` heredado (Postgres directo o GeoServer + `forms/*.ui` + `nn.py`).
Las capas leen y escriben en polizador (`/gdu/oapif/`). Las escrituras pasan por Django, así que valen
los permisos, la validación de los modelos, `updated_by` y el historial.

No se edita a mano: lo genera `armar_proyecto.py` a partir de los schemas del servidor. Si cambia
el servidor (una colección o un campo nuevo), se vuelve a generar.

## Para cada usuario (una sola vez)

1. Pedir el alta en el grupo **GDU: Editores QGIS** (o **GDU: Lectores QGIS** para solo consultar).
   En el servidor:
   `python manage.py configurar_grupos_qgis --editores <usuario> --lectores <usuario>`.
2. En QGIS, en *Configuración → Opciones → Autenticación*, agregar una configuración (**+**):
   - tipo **Basic**;
   - nombre "GDU OAPIF";
   - usuario y clave de polizador (los de la red, por LDAP);
   - el **Id** tiene que ser exactamente `gduoapf`. Se edita destrabando el candado junto al campo.
3. Descargar `gdu-oapif.qgz` desde el visor (botón **Proyecto QGIS**) y abrirlo. No lleva carpeta `forms/` al lado.
   La descarga es este mismo archivo, con las capas apuntando al servidor desde el que se baja
   (`gdu:descargar_proyecto_qgis` le cambia la URL); por eso el versionado puede generarse contra el de desarrollo.

## Tablas de atributos de las capas grandes

La tabla de atributos de QGIS no carga a demanda: al abrirla baja la capa entera (catastro urbano son
430.000 filas, unos 250 MB). Para trabajar sobre una zona, abrirla con el filtro **Mostrar objetos
visibles en el mapa**: así QGIS pide solo lo que está en pantalla. Se puede dejar como comportamiento
por defecto en *Configuración → Opciones → Fuentes de datos → Comportamiento de la tabla de atributos*.

## Reglas de edición

- **Guardar después de cada alta.** QGIS no guarda en una sola transacción: si falla un guardado con
  varias altas, las que ya se mandaron quedan guardadas, y al reintentar se duplican. Si un guardado
  falla, hay que hacer *Descartar cambios*, recargar la capa y volver a cargar lo que faltaba.
- El motivo de un rechazo (campo obligatorio, largo máximo, registro duplicado, "No se puede borrar:
  lo referencian …") aparece en la barra de mensajes. Si QGIS solo dice "Cannot modify feature",
  está en *Ver → Paneles → Registro de mensajes*, pestaña OAPIF.
- Las parcelas están partidas por departamento (y Resistencia en cuatro) para no bajar la provincia
  entera. Una parcela se puede editar desde la capa de su zona o desde "Parcelas (completa)".
- Las listas del formulario (ejecutores e inspectores de una intervención, planos, UF de una parcela,
  etc.) guardan en la tabla intermedia, que también hay que guardar.

## Regenerar el proyecto

En la máquina con QGIS (3.44 LTR o más nuevo), sin abrir QGIS:

```
"C:\Program Files\QGIS 3.44.14\bin\python-qgis-ltr.bat" armar_proyecto.py ^
    --url https://<servidor>/gdu/oapif/ --usuario <usuario del grupo Lectores> --salida gdu-oapif.qgz
```

La clave se pide por consola (o se pasa en `GDU_OAPIF_CLAVE`). El usuario solo se usa para leer los
schemas: el proyecto guarda el id `gduoapf`, no la clave.

En `armar_proyecto.py` se decide lo que el servidor no sabe:

- `GRUPOS`: el panel de capas;
- `VISIBLES`: qué se ve al abrir;
- `ESCALAS`: a partir de qué escala se dibujan las capas grandes;
- `MOSTRAR`: cómo se muestra cada registro en los combos;
- `LISTAS`: qué listas hijas lleva cada formulario.

`polizador/gdu/tests.py` verifica que toda colección que use el `.qgz` exista en el servidor.
