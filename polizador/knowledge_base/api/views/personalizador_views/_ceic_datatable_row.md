---
symbol: _ceic_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 395-402
signature_hash: sha1:d4b96c0307b9b11d6802f728975691294f643612
authored: true
---
# _ceic_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 395-402)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `CEIC`: id + código.

## Firma

```python
def _ceic_datatable_row(c: CEIC, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, CEIC, ...)` (misma sección del módulo).

## Ver también

- [CEIC](../../../personalizador/models/CEIC.md)