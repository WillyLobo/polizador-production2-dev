---
symbol: _categoria_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 329-336
signature_hash: sha1:c8ea5c759293efc7187a03e82330c8eb1f9fe67d
authored: true
---
# _categoria_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 329-336)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Categoria`: código + nombre.

## Firma

```python
def _categoria_datatable_row(c: Categoria, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Categoria, ...)` (misma sección del módulo).

## Ver también

- [Categoria](../../../personalizador/models/Categoria.md)