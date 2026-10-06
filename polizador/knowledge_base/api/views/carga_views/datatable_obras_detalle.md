---
symbol: datatable_obras_detalle
kind: function
module: api/views/carga_views.py
lines: 922-932
signature_hash: sha1:1816c427384386354797bbea6b44097fc8b708de
authored: true
---

# datatable_obras_detalle

**Módulo:** `api/views/carga_views.py` (líneas 922-932)

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
