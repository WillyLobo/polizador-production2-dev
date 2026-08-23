---
symbol: create_incorporacion
kind: function
module: api/views/secretariador_views.py
lines: 829-830
signature_hash: sha1:3b720ccf2d35b4dd4b4f6a61b5bc53987228b5ed
authored: true
---

# create_incorporacion

**Módulo:** `api/views/secretariador_views.py` (líneas 829-830)

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
