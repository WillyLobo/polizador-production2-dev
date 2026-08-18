---
symbol: _actividadespecifica_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 447-459
signature_hash: sha1:3d77969de838e3fb0af2fe339703403d72990ee5
authored: true
---

# _actividadespecifica_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 447-459)

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
