---
symbol: create_monto_viatico
kind: function
module: api/views/secretariador_views.py
lines: 448-449
signature_hash: sha1:a73a8b6bd65f5e5e0d7474a716e5082b911a8d05
authored: true
---

# create_monto_viatico

**Módulo:** `api/views/secretariador_views.py` (líneas 448-449)

## Propósito

Alta de `MontoViaticoDiario` desde `MontoViaticoDiarioCreate` (`payload.model_dump()` directo a `MontoViaticoDiario.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_monto_viatico(request, payload: MontoViaticoCreate):
```

## Uso real

`POST /v1/api/montos-viaticos/` — response=`MontoViaticoDiarioOut`.

## Ver también

- [MontoViaticoDiario](../../../secretariador/models/MontoViaticoDiario.md)
