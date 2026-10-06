---
symbol: create_contrato
kind: function
module: api/views/carga_views.py
lines: 1607-1608
signature_hash: sha1:68a42491419e63e6cf1b75788f00e3c360887c17
authored: true
---

# create_contrato

**Módulo:** `api/views/carga_views.py` (líneas 1607-1608)

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
