---
symbol: create_provincia
kind: function
module: api/views/carga_views.py
lines: 378-379
signature_hash: sha1:fb6f41161af503c22c6c5eb08816c131b5b3692e
authored: true
---

# create_provincia

**Módulo:** `api/views/carga_views.py` (líneas 378-379)

## Propósito

Alta de `Provincia` desde `ProvinciaCreate` (`payload.model_dump()` directo a `Provincia.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_provincia(request, payload: ProvinciaCreate):
```

## Uso real

`POST /v1/api/provincias/` — response=`ProvinciaOut`.

## Ver también

- [Provincia](../../../carga/models/Provincia.md)
