---
symbol: datatable_obras_detalle
kind: function
module: api/views/carga_views.py
lines: 921-931
signature_hash: sha1:c65202f015a7ba2526bcde0fcaf253abd040268d
authored: true
---

# datatable_obras_detalle

**Módulo:** `api/views/carga_views.py` (líneas 921-931)

## Propósito

Expansión de fila del datatable de Obras: renderiza `ajax_datatable/carga/obra/render_row_details.html` con la Obra (y su `obra_madre`) precargada.

## Firma

```python
def datatable_obras_detalle(request, id: int):
```

## Uso real

`GET /v1/api/datatables/obras/{id}/detalle/`.

## Ver también

- [Obra](../../../carga/models/Obra.md)
