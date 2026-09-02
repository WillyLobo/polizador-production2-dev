---
symbol: FormValidationErrorListView
kind: class
module: core/views.py
lines: 31-32
signature_hash: sha1:462312a7aea980b56bc289e07dd6c2a698b8bb4a
authored: true
---

# FormValidationErrorListView

**Módulo:** `core/views.py` (líneas 31-32)

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
