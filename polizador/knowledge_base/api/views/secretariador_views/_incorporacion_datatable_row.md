---
symbol: _incorporacion_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 840-859
signature_hash: sha1:3abdb26da8f6cb50a1ab82c5135351182005b7aa
authored: true
---

# _incorporacion_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 840-859)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Incorporacion`: actuación, Solicitud de origen, solicitante.

## Firma

```python
def _incorporacion_datatable_row(i: Incorporacion, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Incorporacion, ...)` (misma sección del módulo).

## Ver también

- [Incorporacion](../../../secretariador/models/Incorporacion.md)
