---
symbol: _directorio_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 491-504
signature_hash: sha1:2a1da9a67e1226f9602469c8bd1be2d784ba8597
authored: true
---
# _directorio_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 491-504)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Directorio`: nombre, autoridad a cargo, CUOF.

## Firma

```python
def _directorio_datatable_row(d: Directorio, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Directorio, ...)` (misma sección del módulo).

## Ver también

- [Directorio](../../../personalizador/models/Directorio.md)