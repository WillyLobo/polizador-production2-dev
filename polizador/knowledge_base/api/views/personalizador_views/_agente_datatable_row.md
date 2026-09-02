---
symbol: _agente_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 693-716
signature_hash: sha1:20df6f5327f562bd3149dd828fc18ff33896099b
authored: true
---
# _agente_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 693-716)

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