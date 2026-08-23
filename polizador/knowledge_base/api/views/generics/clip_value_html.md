---
symbol: clip_value_html
kind: function
module: api/views/generics.py
lines: 59-67
signature_hash: sha1:264d2d76346d11b14e3b610f3103765948f0d678
authored: true
---

# clip_value_html

**Módulo:** `api/views/generics.py` (líneas 59-67)

## Propósito

Replica el truncado de columna `max_length` de `django-ajax-datatable`: envuelve el valor en `<span title="texto completo">` y corta el texto visible con "…" — para preservar el mismo comportamiento visual (hover para ver completo) que tenían los `AjaxDatatableView` que estos endpoints reemplazaron.

## Firma

```python
def clip_value_html(text, max_length: int) -> str:
```

## Uso real

`_obra_ext_datatable_row`, `_memorandum_datatable_row`, `_resolucion_datatable_row`, `_solicitud_datatable_row`, y otros row-builders con columnas de texto largo.

## Ver también

_(sin referencias cruzadas)_
