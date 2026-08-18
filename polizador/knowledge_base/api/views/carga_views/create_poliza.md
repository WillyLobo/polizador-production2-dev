---
symbol: create_poliza
kind: function
module: api/views/carga_views.py
lines: 1824-1825
signature_hash: sha1:328fc5a1f5d095b3c889c1d7a7b5d1061b963d8e
authored: true
---

# create_poliza

**Módulo:** `api/views/carga_views.py` (líneas 1824-1825)

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
