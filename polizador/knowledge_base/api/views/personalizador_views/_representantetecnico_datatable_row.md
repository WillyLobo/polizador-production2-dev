---
symbol: _representantetecnico_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 116-136
signature_hash: sha1:27725a7795737d3521bdc463508b6f98e9391a29
authored: true
---

# _representantetecnico_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 116-136)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `RepresentanteTecnico`: nombre, apellido, DNI, CUIT, profesión, matrícula.

## Firma

```python
def _representantetecnico_datatable_row(r: RepresentanteTecnico, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, RepresentanteTecnico, ...)` (misma sección del módulo).

## Ver también

- [RepresentanteTecnico](../../../personalizador/models/RepresentanteTecnico.md)
