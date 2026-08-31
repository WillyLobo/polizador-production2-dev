---
symbol: FormValidationError
kind: class
module: core/models.py
lines: 116-140
signature_hash: sha1:3da4c5c0da3d63ffd48407313690262a4b829479
authored: true
---

# FormValidationError

**Módulo:** `core/models.py` (líneas 116-140)

## Propósito

Registra el POST crudo y los errores de un formulario (o formset) que no pasó
`is_valid()` en una vista basada en `LogInvalidFormMixin`, para poder reconstruir a mano
qué mandó el usuario durante debug de sesiones — complementa el log a
`logs/validation_errors.log` que hace el mismo mixin, pero queda consultable/filtrable
desde la UI de administración.

## Firma

```python
class FormValidationError(models.Model):
```

Campos relevantes: `form_class_path` (dotted path para re-importar la clase del form con
`import_string`; vacío si el form es dinámico y no tiene path estable, ej.
`build_matriz_form`), `form_errors` (JSON de `form.errors`), `formsets` (lista de
`{"prefix", "class_path", "errors"}` por cada formset asociado), `raw_data` (dict
`{campo: [valores...]}`, siempre listas para soportar campos multivaluados).

## Uso real

Sin candidatos de uso interno detectados por grep en `models.py`/`views.py`/`forms.py`
(el `create()` vive en `core/mixins.py`, fuera del alcance de este grep mecánico).

## Flujo de datos

`LogInvalidFormMixin._log_form_debug` (core/mixins.py) crea el registro cuando un form o
formset falla validación en una vista CBV → `core.form_debug.build_ficha(record)` lo
humaniza para el detalle (resuelve `form_class_path` y traduce cada valor crudo según el
tipo de campo) → listado/detalle vía la API (`datatable_errores_validacion*`) →
`FormValidationErrorListView`. El management command `purgar_errores_validacion` borra
los registros con más de 90 días (default) de antigüedad.

## Ver también

- [FormValidationErrorListView](../../core/views/FormValidationErrorListView.md) — vista de administración que lista estos registros.
- [datatable_errores_validacion](../../api/views/core_views/datatable_errores_validacion.md) — endpoint de listado/filtro.
- [datatable_errores_validacion_detalle](../../api/views/core_views/datatable_errores_validacion_detalle.md) — endpoint de detalle.
