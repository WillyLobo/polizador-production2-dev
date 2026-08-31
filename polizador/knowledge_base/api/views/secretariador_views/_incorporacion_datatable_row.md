---
symbol: _incorporacion_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 847-866
signature_hash: sha1:1a119d2c625773dce55b5d0fa248a69c4a4bb7cb
authored: true
---
# _incorporacion_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 847-866)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Incorporacion`: actuación, Solicitud de origen, solicitante.

## Firma

```python
def _incorporacion_datatable_row(i: Incorporacion, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Incorporacion, ...)` (misma sección del módulo).

## Ver también

- [Incorporacion](../../../secretariador/models/Incorporacion.md)