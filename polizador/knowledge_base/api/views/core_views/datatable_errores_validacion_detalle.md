---
symbol: datatable_errores_validacion_detalle
kind: function
module: api/views/core_views.py
lines: 61-68
signature_hash: sha1:627d837c99512e4d2a6a02845617009db51c5c39
authored: true
---

# datatable_errores_validacion_detalle

**Módulo:** `api/views/core_views.py` (líneas 61-68)

## Propósito

Endpoint ninja (`GET /v1/api/core/datatables/errores-validacion/{id}/detalle/`) que
arma el HTML del detalle expandible de un `FormValidationError` puntual, humanizando el
POST crudo que se guardó al momento del fallo de validación. Restringido a superusers.

## Firma

```python
def datatable_errores_validacion_detalle(request, id: int):
```

## Uso real

Sin candidatos de uso interno detectados por grep (lo llama el JS de ajax-datatable al
expandir una fila en `errores_validacion/list.html`, no otro código Python).

## Flujo de datos

`get_object_or_404(FormValidationError.objects.select_related("user"), id=id)` →
`core.form_debug.build_ficha(record)` (resuelve la form_class original vía
`import_string` a partir de `form_class_path` y humaniza cada valor crudo según el tipo
de campo declarado) → `render_to_string` con el template
`ajax_datatable/core/formvalidationerror/render_row_details.html` → `{"html": ...}`.

## Ver también

- [datatable_errores_validacion](../core_views/datatable_errores_validacion.md) — endpoint de listado; este es su detalle.
- [FormValidationError](../../../core/models/FormValidationError.md) — modelo consultado.
