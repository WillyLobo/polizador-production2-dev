---
symbol: _agente_comisionado_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 170-190
signature_hash: sha1:c84606bf93bf76373f21bd6bea6566b0be89b11c
authored: true
---

# _agente_comisionado_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 170-190)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Agente`: variante "comisionados" (apellidos, nombres, oficina, CUIT, flags transitorio/gabinete) — distinta de `_agente_datatable_row` (el listado de RRHH completo, más abajo).

## Firma

```python
def _agente_comisionado_datatable_row(a: Agente, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Agente, ...)` (misma sección del módulo).

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
