---
symbol: create_region
kind: function
module: api/views/carga_views.py
lines: 415-416
signature_hash: sha1:3ff8abf682fac94d7433d9bfcff736dc26e9bb76
authored: true
---

# create_region

**Módulo:** `api/views/carga_views.py` (líneas 415-416)

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
