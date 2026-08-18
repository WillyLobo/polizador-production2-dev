---
symbol: _directorio_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 501-514
signature_hash: sha1:8d1970eab024d2af18bc64cd0b4e79af7ec90ce7
authored: true
---

# _directorio_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 501-514)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Directorio`: nombre, autoridad a cargo, CUOF.

## Firma

```python
def _directorio_datatable_row(d: Directorio, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Directorio, ...)` (misma sección del módulo).

## Ver también

- [Directorio](../../../personalizador/models/Directorio.md)
