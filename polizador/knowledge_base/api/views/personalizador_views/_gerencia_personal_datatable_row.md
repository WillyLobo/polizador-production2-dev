---
symbol: _gerencia_personal_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 536-549
signature_hash: sha1:02ba68476044ac5630657de09cd4331474a82c68
authored: true
---

# _gerencia_personal_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 536-549)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Gerencia`: nombre, Directorio, CUOF.

## Firma

```python
def _gerencia_personal_datatable_row(g: Gerencia, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Gerencia, ...)` (misma sección del módulo).

## Ver también

- [Gerencia](../../../personalizador/models/Gerencia.md)
