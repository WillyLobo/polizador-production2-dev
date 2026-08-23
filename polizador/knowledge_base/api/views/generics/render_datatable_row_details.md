---
symbol: render_datatable_row_details
kind: function
module: api/views/generics.py
lines: 77-99
signature_hash: sha1:eab19adf63d51898c9e94326be5b6bdd73be3478
authored: true
---

# render_datatable_row_details

**Módulo:** `api/views/generics.py` (líneas 77-99)

## Propósito

Renderiza la expansión de fila de un datatable: un template específico `ajax_datatable/<app>/<model>/render_row_details.html` si existe, si no un dump genérico campo/valor (mismo comportamiento default que `AjaxDatatableView.render_row_details` del paquete que este endpoint reemplaza) — incluye M2M como texto separado por comas.

## Firma

```python
def render_datatable_row_details(model, obj, request) -> str:
```

## Uso real

`register_simple_datatable`'s `_detalle` endpoint interno (mismo módulo, más abajo).

## Ver también

- [register_simple_datatable](register_simple_datatable.md)
