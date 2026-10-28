# Mapeos del ETL GDU

Tablas de correspondencia que aplica `python manage.py importar_gdu_legacy`. Se
versionan acá para que el área pueda revisarlas y corregirlas sin tocar código.

- `programa_origen.csv`: valor de `programa.origen` en la base heredada (texto libre)
  → `Programa.Origen`. Un valor que no figure acá se carga vacío y aparece en el reporte.
- `localidad.csv`: excepciones al mapeo automático de `localidad` heredada →
  `carga.Localidad`. Por defecto se usa el código INDEC (codpcia + coddpto + codloc,
  que es la PK de `carga.Localidad`); agregar una fila solo si ese código no existe
  en `carga` o apunta a otra localidad.
- `usuarios_qgis.csv`: quién edita (`editor`) o consulta (`lector`) en el proyecto QGIS.
  Sale de los GRANT de escritura sobre las tablas de GDU de la base heredada (en QGIS cada
  editor entraba a Postgres con su usuario; los roles del visor no lo reflejan). Los GRANT
  no sobreviven al restaurar el dump sin esos roles, por eso se conservan acá. Además, todo
  usuario del visor queda en "GDU: Lectores QGIS". Un usuario del CSV sin cuenta en
  polizador no se crea: aparece en el reporte, y después de darlo de alta se le asigna el
  grupo con `configurar_grupos_qgis --editores <usuario>`.
