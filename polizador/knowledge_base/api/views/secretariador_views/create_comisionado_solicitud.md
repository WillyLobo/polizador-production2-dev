---
symbol: create_comisionado_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 812-813
signature_hash: sha1:07d58bb02e8888b74fdc0ed8769109296d789cad
authored: true
---
# create_comisionado_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 812-813)

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