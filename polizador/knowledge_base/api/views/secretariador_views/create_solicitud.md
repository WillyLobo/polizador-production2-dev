---
symbol: create_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 602-608
signature_hash: sha1:1ce0685736d5ff96e022759237fd98b990d44209
authored: true
---

# create_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 602-608)

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
