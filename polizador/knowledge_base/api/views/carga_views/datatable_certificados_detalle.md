---
symbol: datatable_certificados_detalle
kind: function
module: api/views/carga_views.py
lines: 1403-1410
signature_hash: sha1:05c8f6c26fca1a9b6b842c49c1dd762795b3dac8
authored: true
---

# datatable_certificados_detalle

**Módulo:** `api/views/carga_views.py` (líneas 1403-1410)

## Propósito

Expansión de fila del datatable de Certificados.

## Firma

```python
def datatable_certificados_detalle(request, id: int):
```

## Uso real

`GET /v1/api/datatables/certificados/{id}/detalle/`.

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
