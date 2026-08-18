---
symbol: create_contrato_rubro
kind: function
module: api/views/carga_views.py
lines: 1671-1672
signature_hash: sha1:d79e5cc45832ebfb7a7f8f665b50ece6b849cd9c
authored: true
---

# create_contrato_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1671-1672)

## Propósito

Alta de `ContratoRubro` desde `ContratoRubroCreate` (`payload.model_dump()` directo a `ContratoRubro.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_contrato_rubro(request, payload: ContratoRubroCreate):
```

## Uso real

`POST /v1/api/contrato-rubros/` — response=`ContratoRubroOut`.

## Ver también

- [ContratoRubro](../../../carga/models/ContratoRubro.md)
