---
symbol: _denominacioncargo_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 353-360
signature_hash: sha1:370e57703527a719abf90fb7e1724b1ce2e65f06
authored: true
---
# _denominacioncargo_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 353-360)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `DenominacionCargo`: id + denominación.

## Firma

```python
def _denominacioncargo_datatable_row(d: DenominacionCargo, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, DenominacionCargo, ...)` (misma sección del módulo).

## Ver también

- [DenominacionCargo](../../../personalizador/models/DenominacionCargo.md)