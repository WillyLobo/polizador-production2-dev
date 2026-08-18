---
symbol: create_indec
kind: function
module: api/views/carga_views.py
lines: 1782-1783
signature_hash: sha1:f0a426a349ab565e6306552659d4e8e9b21ee180
authored: true
---

# create_indec

**Módulo:** `api/views/carga_views.py` (líneas 1782-1783)

## Propósito

Alta de `INDEC` desde `INDECCreate` (`payload.model_dump()` directo a `INDEC.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_indec(request, payload: INDECCreate):
```

## Uso real

`POST /v1/api/indec/` — response=`INDECOut`.

## Ver también

- [INDEC](../../../carga/models/INDEC.md)
