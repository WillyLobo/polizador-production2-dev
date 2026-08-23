---
symbol: _conjunto_datatable_row
kind: function
module: api/views/carga_views.py
lines: 1507-1524
signature_hash: sha1:d46dd0d3c087292d556a9f6c1468663e494f7930
authored: true
---

# _conjunto_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 1507-1524)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `ConjuntoLicitado`: nombre, resolución, subconjunto.

## Firma

```python
def _conjunto_datatable_row(c: ConjuntoLicitado, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, ConjuntoLicitado, ...)` (misma sección del módulo).

## Ver también

- [ConjuntoLicitado](../../../carga/models/ConjuntoLicitado.md)
