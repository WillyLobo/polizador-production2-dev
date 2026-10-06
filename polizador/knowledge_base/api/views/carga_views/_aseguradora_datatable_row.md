---
symbol: _aseguradora_datatable_row
kind: function
module: api/views/carga_views.py
lines: 194-205
signature_hash: sha1:a2aeb5f19809eba96731394d7d275509ec511460
authored: true
---

# _aseguradora_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 194-205)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Aseguradora`: id + nombre.

## Firma

```python
def _aseguradora_datatable_row(a: Aseguradora, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Aseguradora, ...)` (misma sección del módulo).

## Ver también

- [Aseguradora](../../../carga/models/Aseguradora.md)
