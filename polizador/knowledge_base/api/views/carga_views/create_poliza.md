---
symbol: create_poliza
kind: function
module: api/views/carga_views.py
lines: 1845-1846
signature_hash: sha1:6c9c1c7c504bac9091438f2640c9c8ff9e43aac2
authored: true
---

# create_poliza

**Módulo:** `api/views/carga_views.py` (líneas 1845-1846)

## Propósito

Alta de `Poliza` desde `PolizaCreate` (`payload.model_dump()` directo a `Poliza.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_poliza(request, payload: PolizaCreate):
```

## Uso real

`POST /v1/api/polizas/` — response=`PolizaOut`.

## Ver también

- [Poliza](../../../carga/models/Poliza.md)
