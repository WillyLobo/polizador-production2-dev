---
symbol: _direccion_personal_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 573-586
signature_hash: sha1:e21564540ae014692834c7fb1168d0794bafcd78
authored: true
---

# _direccion_personal_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 573-586)

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
