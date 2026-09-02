---
symbol: _actividadespecifica_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 437-449
signature_hash: sha1:f6e9c2ee10097e5bc145bc3b71f77e9264553da9
authored: true
---
# _actividadespecifica_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 437-449)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `ActividadEspecifica`: código + nombre.

## Firma

```python
def _actividadespecifica_datatable_row(a: ActividadEspecifica, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, ActividadEspecifica, ...)` (misma sección del módulo).

## Ver también

- [ActividadEspecifica](../../../personalizador/models/ActividadEspecifica.md)