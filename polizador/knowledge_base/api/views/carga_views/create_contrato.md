---
symbol: create_contrato
kind: function
module: api/views/carga_views.py
lines: 1606-1607
signature_hash: sha1:ccac06764a9f7bd33ebbd4b61b531eff8c3ff3ed
authored: true
---

# create_contrato

**Módulo:** `api/views/carga_views.py` (líneas 1606-1607)

## Propósito

Alta de `Contrato` desde `ContratoCreate` (`payload.model_dump()` directo a `Contrato.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_contrato(request, payload: ContratoCreate):
```

## Uso real

`POST /v1/api/contratos/` — response=`ContratoOut`.

## Ver también

- [Contrato](../../../carga/models/Contrato.md)
