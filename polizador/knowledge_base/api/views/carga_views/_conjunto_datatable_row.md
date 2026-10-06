---
symbol: _conjunto_datatable_row
kind: function
module: api/views/carga_views.py
lines: 1508-1525
signature_hash: sha1:87407c66d8c5dca448a79a78b982813708f16623
authored: true
---

# _conjunto_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 1508-1525)

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
