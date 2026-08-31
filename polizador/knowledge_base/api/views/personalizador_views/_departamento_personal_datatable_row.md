---
symbol: _departamento_personal_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 600-613
signature_hash: sha1:d38beea8e909378f073ee85d57098f7b6d122e8a
authored: true
---
# _departamento_personal_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 600-613)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Departamento`: nombre, Dirección, CUOF.

## Firma

```python
def _departamento_personal_datatable_row(d: Departamento, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Departamento, ...)` (misma sección del módulo).

## Ver también

- [Departamento](../../../personalizador/models/Departamento.md)