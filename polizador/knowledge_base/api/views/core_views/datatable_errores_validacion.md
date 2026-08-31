---
symbol: datatable_errores_validacion
kind: function
module: api/views/core_views.py
lines: 36-56
signature_hash: sha1:31375c595406987f3a028732f84705ca71cdd353
authored: true
---

# datatable_errores_validacion

**Módulo:** `api/views/core_views.py` (líneas 36-56)

## Propósito

Endpoint ninja (`GET /v1/api/core/datatables/errores-validacion/`) que alimenta el
datatable de `FormValidationErrorListView`: pagina, filtra y ordena registros de
`FormValidationError`. Restringido a superusers vía `@decorate_view(require_superuser)`.

## Firma

```python
def datatable_errores_validacion(request, draw: int=1, start: int=0, length: int=50, search: str='', order_by: str='-created_at'):
```

## Uso real

Sin candidatos de uso interno detectados por grep (se llama desde el JS de
ajax-datatable en `errores_validacion/list.html`, no desde otro código Python).

## Flujo de datos

`FormValidationError.objects.select_related("user")` → filtro `Q` sobre
`view_name`/`path`/`user__username` si hay `search` → `order_by` validado contra la
whitelist `_ORDER_FIELDS` vía `parse_order_by` (evita ordenar por un campo arbitrario no
whitelisteado) → slice `[start:start+length]` (o `[start:]` si `length == -1`) → cada
registro de la página pasa por `_row` → payload estilo DataTables
(`draw`/`recordsTotal`/`recordsFiltered`/`data`).

## Ver también

- [_row](../core_views/_row.md) — serializa cada fila.
- [datatable_errores_validacion_detalle](../core_views/datatable_errores_validacion_detalle.md) — detalle expandible de una fila.
- [FormValidationErrorListView](../../../core/views/FormValidationErrorListView.md) — vista que sirve el template que consume este endpoint.
