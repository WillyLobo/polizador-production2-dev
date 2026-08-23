---
symbol: _localidad_datatable_row
kind: function
module: api/views/carga_views.py
lines: 642-660
signature_hash: sha1:a572e9c39704c3c32f302d125e48281fda768e55
authored: true
---

# _localidad_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 642-660)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Localidad`: nombre, Municipio, Departamento, función.

## Firma

```python
def _localidad_datatable_row(l: Localidad, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Localidad, ...)` (misma sección del módulo).

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
