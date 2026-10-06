---
symbol: create_area
kind: function
module: api/views/carga_views.py
lines: 136-137
signature_hash: sha1:c8d71377bbfc8c687aab10d20626c5ab2253ab98
authored: true
---

# create_area

**Módulo:** `api/views/carga_views.py` (líneas 136-137)

## Propósito

Alta de `Area` desde `AreaCreate` (`payload.model_dump()` directo a `Area.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_area(request, payload: AreaCreate):
```

## Uso real

`POST /v1/api/areas/` — response=`AreaOut`.

## Ver también

- [Area](../../../carga/models/Area.md)
