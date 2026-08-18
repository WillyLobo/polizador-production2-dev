---
symbol: _agente_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 703-726
signature_hash: sha1:318170e579f41ebae357e1d85ab0dbc7dabdb153
authored: true
---

# _agente_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 703-726)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. El listado de RRHH completo (no el de "comisionados" — ver `_agente_comisionado_datatable_row`): apellidos, nombres, DNI, denominación de cargo, oficina, edad (`edad_calculada`, ver `_EdadCalculada`), antigüedad formateada (`_formatear_antiguedad`), y flags activo/con_errores.

## Firma

```python
def _agente_datatable_row(a: Agente, user) -> dict:
```

## Uso real

`register_simple_datatable(router, Agente, "agentes", ..., with_detail=False)` — el detalle de fila lo maneja `datatable_agentes_detalle` aparte (más abajo), no el mecanismo genérico.

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
- [_EdadCalculada](_EdadCalculada.md)
- [_formatear_antiguedad](_formatear_antiguedad.md)
