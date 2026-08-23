---
symbol: create_region
kind: function
module: api/views/carga_views.py
lines: 414-415
signature_hash: sha1:48b266a6187b434b07ceeb2d22e1d0058b868860
authored: true
---

# create_region

**Módulo:** `api/views/carga_views.py` (líneas 414-415)

## Propósito

Alta de `Region` desde `RegionCreate` (`payload.model_dump()` directo a `Region.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_region(request, payload: RegionCreate):
```

## Uso real

`POST /v1/api/regiones/` — response=`RegionOut`.

## Ver también

- [Region](../../../carga/models/Region.md)
