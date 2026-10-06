---
symbol: _programa_datatable_row
kind: function
module: api/views/carga_views.py
lines: 339-350
signature_hash: sha1:0cb31d3e8b0da3d13d79092f34fe2e233be10128
authored: true
---

# _programa_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 339-350)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Programa`: id + nombre.

## Firma

```python
def _programa_datatable_row(p: Programa, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Programa, ...)` (misma sección del módulo).

## Ver también

- [Programa](../../../carga/models/Programa.md)
