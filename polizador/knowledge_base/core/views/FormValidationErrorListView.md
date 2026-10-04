---
symbol: FormValidationErrorListView
kind: class
module: core/views.py
lines: 54-55
signature_hash: sha1:f34ed4ea64fc8f675688b9e2a5143c03ede76a4d
authored: true
---

# FormValidationErrorListView

**Módulo:** `core/views.py` (líneas 54-55)

## Propósito

Vista de administración, solo para superusers, que sirve la página con el datatable de
errores de validación de formularios capturados por `LogInvalidFormMixin`. Sin lógica
propia — es un `TemplateView` puro; el listado y detalle los sirve la API por AJAX.

## Firma

```python
class FormValidationErrorListView(SuperuserRequiredMixin, TemplateView):
```

## Uso real

Registrada en `polizador/urls.py` como
`path("administracion/errores-validacion/", FormValidationErrorListView.as_view(), name="form_validation_errors")`.
Sin candidatos de uso interno detectados por grep.

## Flujo de datos

Renderiza `errores_validacion/list.html`, cuyo JS (ajax-datatable) consume
`datatable_errores_validacion` y `datatable_errores_validacion_detalle` (api app) para
listar y expandir registros de `FormValidationError` — esta vista no toca esos datos
directamente.

## Ver también

- [FormValidationError](../../core/models/FormValidationError.md) — modelo listado.
- [datatable_errores_validacion](../../api/views/core_views/datatable_errores_validacion.md) — endpoint que alimenta el datatable de esta vista.
