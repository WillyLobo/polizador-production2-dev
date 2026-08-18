---
symbol: _apartadocargo_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 384-391
signature_hash: sha1:3a2afb7f70561a3d6a931a25cad92cfb141d5719
authored: true
---

# _apartadocargo_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 384-391)

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
