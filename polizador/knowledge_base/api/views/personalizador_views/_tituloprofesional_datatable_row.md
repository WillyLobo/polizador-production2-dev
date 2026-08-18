---
symbol: _tituloprofesional_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 303-316
signature_hash: sha1:f2bc1d6014f034a26ea3d31d706f4f9d6ddfab20
authored: true
---

# _tituloprofesional_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 303-316)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `TituloProfesional`: nombre, abreviatura, grado.

## Firma

```python
def _tituloprofesional_datatable_row(t: TituloProfesional, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, TituloProfesional, ...)` (misma sección del módulo).

## Ver también

- [TituloProfesional](../../../personalizador/models/TituloProfesional.md)
