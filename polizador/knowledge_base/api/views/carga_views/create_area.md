---
symbol: create_area
kind: function
module: api/views/carga_views.py
lines: 135-136
signature_hash: sha1:bd39f918ef587cdd1da735ebcb7ade1ef5e97990
authored: true
---

# create_area

**Módulo:** `api/views/carga_views.py` (líneas 135-136)

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
