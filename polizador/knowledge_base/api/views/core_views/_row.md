---
symbol: _row
kind: function
module: api/views/core_views.py
lines: 24-31
signature_hash: sha1:4c8462c73837bc36dff550373f0e6eb358bb94d3
authored: true
---

# _row

**Módulo:** `api/views/core_views.py` (líneas 24-31)

## Propósito

Serializa un `FormValidationError` a un dict plano para una fila del datatable de
errores de validación: id, fecha formateada, usuario (o "—" si es anónimo), nombre corto
de la vista (último segmento del dotted path) y path de la request.

## Firma

```python
def _row(o):
```

## Uso real

Usado por `datatable_errores_validacion` para armar la lista `data` de la respuesta
paginada. Candidatos detectados automáticamente:

- `api/views/core_views.py:55` — `"data": [_row(o) for o in page],`

## Flujo de datos

`FormValidationError` (core.models, ya con `select_related("user")` en el queryset del
caller) → dict de fila → lista `data` del payload JSON estilo DataTables → tabla
ajax-datatable en `errores_validacion/list.html`.

## Ver también

- [datatable_errores_validacion](../core_views/datatable_errores_validacion.md) — único caller.
- [FormValidationError](../../../core/models/FormValidationError.md) — modelo serializado.
