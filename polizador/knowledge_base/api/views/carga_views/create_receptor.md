---
symbol: create_receptor
kind: function
module: api/views/carga_views.py
lines: 99-100
signature_hash: sha1:e87ad45b36c1228fc541f99dfb2aa05df8300455
authored: true
---

# create_receptor

**Módulo:** `api/views/carga_views.py` (líneas 99-100)

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
