---
symbol: retrieve_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 603-604
signature_hash: sha1:b531126ebc6575ff9ea9b66e7f98ce46afa27cbd
authored: true
---
# retrieve_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 603-604)

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