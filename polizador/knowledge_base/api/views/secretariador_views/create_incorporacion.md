---
symbol: create_incorporacion
kind: function
module: api/views/secretariador_views.py
lines: 836-837
signature_hash: sha1:c1ad8cf3d9ebe5bd91511701bf77994da146e25b
authored: true
---
# create_incorporacion

**Módulo:** `api/views/secretariador_views.py` (líneas 836-837)

## Propósito

Alta de `Incorporacion` desde `IncorporacionCreate` (`payload.model_dump()` directo a `Incorporacion.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_incorporacion(request, payload: IncorporacionCreate):
```

## Uso real

`POST /v1/api/incorporaciones/` — response=`IncorporacionOut`.

## Ver también

- [Incorporacion](../../../secretariador/models/Incorporacion.md)