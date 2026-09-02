---
symbol: create_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 609-615
signature_hash: sha1:be99d6a1e16935aa192120a66c00274e3bb11d94
authored: true
---
# create_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 609-615)

## Propósito

Alta de Solicitud con manejo explícito del M2M `solicitud_localidades` (mismo patrón que `create_obra`/`create_incorporacion`... salvo que acá no hay `_solicitud_out` dedicado — el M2M se saca del payload como `localidad_ids` y se asigna con `.set()` después de crear).

## Firma

```python
def create_solicitud(request, payload: SolicitudCreate):
```

## Uso real

`POST /v1/api/solicitudes/` — response=`SolicitudOut`.

## Ver también

- [Solicitud](../../../secretariador/models/Solicitud.md)