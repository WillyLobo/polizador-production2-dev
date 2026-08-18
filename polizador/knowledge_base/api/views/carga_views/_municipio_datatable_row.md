---
symbol: _municipio_datatable_row
kind: function
module: api/views/carga_views.py
lines: 559-576
signature_hash: sha1:858818a8038d37e7bce18d1c7ee81284e329cbca
authored: true
---

# _municipio_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 559-576)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Municipio`: nombre, Departamento, Región.

## Firma

```python
def _municipio_datatable_row(m: Municipio, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Municipio, ...)` (misma sección del módulo).

## Ver también

- [Municipio](../../../carga/models/Municipio.md)
