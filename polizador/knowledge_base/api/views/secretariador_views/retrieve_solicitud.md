---
symbol: retrieve_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 596-597
signature_hash: sha1:503da61d441c24c502f20a4c002859ec0e22dac9
authored: true
---

# retrieve_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 596-597)

## Propósito

Devuelve un `Solicitud` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_solicitud(request, id: int):
```

## Uso real

`GET /v1/api/solicitude/{{id}}/` — response=`SolicitudOut`.

## Ver también

- [Solicitud](../../../secretariador/models/Solicitud.md)
