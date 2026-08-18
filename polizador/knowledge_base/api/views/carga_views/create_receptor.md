---
symbol: create_receptor
kind: function
module: api/views/carga_views.py
lines: 98-99
signature_hash: sha1:5e34440f30edeaa1dd68cab02386287039d7b4d5
authored: true
---

# create_receptor

**Módulo:** `api/views/carga_views.py` (líneas 98-99)

## Propósito

Alta de `Receptor` desde `ReceptorCreate` (`payload.model_dump()` directo a `Receptor.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_receptor(request, payload: ReceptorCreate):
```

## Uso real

`POST /v1/api/receptores/` — response=`ReceptorOut`.

## Ver también

- [Receptor](../../../carga/models/Receptor.md)
