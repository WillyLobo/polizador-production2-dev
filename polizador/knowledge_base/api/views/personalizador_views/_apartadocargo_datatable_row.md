---
symbol: _apartadocargo_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 374-381
signature_hash: sha1:827713d00eb1a4840200d283973ae6f250f85d24
authored: true
---
# _apartadocargo_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 374-381)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `ApartadoCargo`: id + denominación.

## Firma

```python
def _apartadocargo_datatable_row(a: ApartadoCargo, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, ApartadoCargo, ...)` (misma sección del módulo).

## Ver también

- [ApartadoCargo](../../../personalizador/models/ApartadoCargo.md)