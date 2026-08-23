---
symbol: _region_datatable_row
kind: function
module: api/views/carga_views.py
lines: 435-446
signature_hash: sha1:45aae3c4350875b3baec0b46441316c9a1e83f6d
authored: true
---

# _region_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 435-446)

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
