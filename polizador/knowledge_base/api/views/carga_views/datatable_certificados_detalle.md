---
symbol: datatable_certificados_detalle
kind: function
module: api/views/carga_views.py
lines: 1404-1411
signature_hash: sha1:7f9894a296c765078b7d850c7f8399b419c7b523
authored: true
---

# datatable_certificados_detalle

**Módulo:** `api/views/carga_views.py` (líneas 1404-1411)

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
