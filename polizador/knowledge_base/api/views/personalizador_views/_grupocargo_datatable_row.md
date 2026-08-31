---
symbol: _grupocargo_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 416-423
signature_hash: sha1:6e9b46844ab9d5245fa740cc8b38acb8b80c0e35
authored: true
---
# _grupocargo_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 416-423)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `GrupoCargo`: id + número.

## Firma

```python
def _grupocargo_datatable_row(g: GrupoCargo, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, GrupoCargo, ...)` (misma sección del módulo).

## Ver también

- [GrupoCargo](../../../personalizador/models/GrupoCargo.md)