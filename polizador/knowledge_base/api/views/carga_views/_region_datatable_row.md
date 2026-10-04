---
symbol: _region_datatable_row
kind: function
module: api/views/carga_views.py
lines: 436-447
signature_hash: sha1:9e1e1ab2e24b367381b04ea79e2b72a0abf5fc39
authored: true
---

# _region_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 436-447)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Region`: id + número de región.

## Firma

```python
def _region_datatable_row(r: Region, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Region, ...)` (misma sección del módulo).

## Ver también

- [Region](../../../carga/models/Region.md)
