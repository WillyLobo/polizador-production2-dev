---
symbol: create_comisionado_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 805-806
signature_hash: sha1:933a5fc735ffa41f9bba974b64253f91e7b52394
authored: true
---

# create_comisionado_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 805-806)

## Propósito

Alta de `ComisionadoSolicitud` desde `ComisionadoSolicitudCreate` (`payload.model_dump()` directo a `ComisionadoSolicitud.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_comisionado_solicitud(request, payload: ComisionadoSolicitudCreate):
```

## Uso real

`POST /v1/api/comisionados-solicitudes/` — response=`ComisionadoSolicitudOut`.

## Ver también

- [ComisionadoSolicitud](../../../secretariador/models/ComisionadoSolicitud.md)
