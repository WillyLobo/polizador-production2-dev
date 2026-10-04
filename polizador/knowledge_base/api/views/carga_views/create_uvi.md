---
symbol: create_uvi
kind: function
module: api/views/carga_views.py
lines: 1763-1764
signature_hash: sha1:8eccacdfe37bd34be8d7c001ba2a0c19ead21df2
authored: true
---

# create_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1763-1764)

## Propósito

Alta de `Uvi` desde `UviCreate` (`payload.model_dump()` directo a `Uvi.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_uvi(request, payload: UviCreate):
```

## Uso real

`POST /v1/api/uvi/` — response=`UviOut`.

## Ver también

- [Uvi](../../../carga/models/Uvi.md)
