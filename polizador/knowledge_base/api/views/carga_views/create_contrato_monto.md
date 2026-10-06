---
symbol: create_contrato_monto
kind: function
module: api/views/carga_views.py
lines: 1661-1662
signature_hash: sha1:49e81b328e0b0c38d63d0208b7d37b0e11a8099d
authored: true
---

# create_contrato_monto

**Módulo:** `api/views/carga_views.py` (líneas 1661-1662)

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
