---
symbol: _direccion_personal_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 563-576
signature_hash: sha1:cbb58f2b3a8459419c18e4451554d6a964f28112
authored: true
---
# _direccion_personal_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 563-576)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Direccion`: nombre, Gerencia, CUOF.

## Firma

```python
def _direccion_personal_datatable_row(d: Direccion, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Direccion, ...)` (misma sección del módulo).

## Ver también

- [Direccion](../../../personalizador/models/Direccion.md)