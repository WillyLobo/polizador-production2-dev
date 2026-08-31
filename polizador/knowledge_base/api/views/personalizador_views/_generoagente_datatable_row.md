---
symbol: _generoagente_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 272-279
signature_hash: sha1:5cf14456da2fefd7f38647bd9beeaf5aac170f6b
authored: true
---
# _generoagente_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 272-279)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `GeneroAgente`: id + nombre.

## Firma

```python
def _generoagente_datatable_row(g: GeneroAgente, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, GeneroAgente, ...)` (misma sección del módulo).

## Ver también

- [GeneroAgente](../../../personalizador/models/GeneroAgente.md)