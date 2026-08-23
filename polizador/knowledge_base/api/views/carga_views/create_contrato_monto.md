---
symbol: create_contrato_monto
kind: function
module: api/views/carga_views.py
lines: 1640-1641
signature_hash: sha1:c5950e5edbc23653133b1dc9c4b3c9813c1cc2c4
authored: true
---

# create_contrato_monto

**Módulo:** `api/views/carga_views.py` (líneas 1640-1641)

## Propósito

Alta de `ContratoMonto` desde `ContratoMontoCreate` (`payload.model_dump()` directo a `ContratoMonto.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_contrato_monto(request, payload: ContratoMontoCreate):
```

## Uso real

`POST /v1/api/contratos-montos/` — response=`ContratoMontoOut`.

## Ver también

- [ContratoMonto](../../../carga/models/ContratoMonto.md)
