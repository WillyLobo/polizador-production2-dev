---
symbol: create_uvi
kind: function
module: api/views/carga_views.py
lines: 1742-1743
signature_hash: sha1:82d3abbfadb545cfdcc54b6a592d99122c7419ec
authored: true
---

# create_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1742-1743)

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
