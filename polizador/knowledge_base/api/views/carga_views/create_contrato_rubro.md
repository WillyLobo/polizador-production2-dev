---
symbol: create_contrato_rubro
kind: function
module: api/views/carga_views.py
lines: 1692-1693
signature_hash: sha1:d4bb829bb7f6736e0e350c45a2a2b83daafa6590
authored: true
---

# create_contrato_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1692-1693)

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
