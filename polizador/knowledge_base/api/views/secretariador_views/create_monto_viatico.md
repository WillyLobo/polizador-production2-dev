---
symbol: create_monto_viatico
kind: function
module: api/views/secretariador_views.py
lines: 455-456
signature_hash: sha1:e103bfcc21b3713ce2f97c7d49e171292a9c3ea3
authored: true
---
# create_monto_viatico

**Módulo:** `api/views/secretariador_views.py` (líneas 455-456)

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