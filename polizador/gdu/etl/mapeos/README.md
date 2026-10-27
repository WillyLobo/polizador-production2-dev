# Mapeos del ETL GDU

Tablas de correspondencia que aplica `python manage.py importar_gdu_legacy`. Se
versionan acá para que el área pueda revisarlas y corregirlas sin tocar código.

- `programa_origen.csv`: valor de `programa.origen` en la base heredada (texto libre)
  → `Programa.Origen`. Un valor que no figure acá se carga vacío y aparece en el reporte.
- `localidad.csv`: excepciones al mapeo automático de `localidad` heredada →
  `carga.Localidad`. Por defecto se usa el código INDEC (codpcia + coddpto + codloc,
  que es la PK de `carga.Localidad`); agregar una fila solo si ese código no existe
  en `carga` o apunta a otra localidad.
