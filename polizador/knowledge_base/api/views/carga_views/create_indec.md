---
symbol: create_indec
kind: function
module: api/views/carga_views.py
lines: 1803-1804
signature_hash: sha1:d7fd61128c7e0b138dfe05e7f20471cb68a7b739
authored: true
---

# create_indec

**Módulo:** `api/views/carga_views.py` (líneas 1803-1804)

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
