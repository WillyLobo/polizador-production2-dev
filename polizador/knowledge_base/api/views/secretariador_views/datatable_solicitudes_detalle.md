---
symbol: datatable_solicitudes_detalle
kind: function
module: api/views/secretariador_views.py
lines: 774-784
signature_hash: sha1:8127a74d788713ed27791308ad5742dcad5a4ba3
authored: true
---
# datatable_solicitudes_detalle

**Módulo:** `api/views/secretariador_views.py` (líneas 774-784)

## Propósito

Expansión de fila del datatable de Solicitudes.

## Firma

```python
def datatable_solicitudes_detalle(request, id: int):
```

## Uso real

`GET /v1/api/datatables/solicitudes/{id}/detalle/`.

## Ver también

- [Solicitud](../../../secretariador/models/Solicitud.md)