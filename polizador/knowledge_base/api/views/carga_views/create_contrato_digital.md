---
symbol: create_contrato_digital
kind: function
module: api/views/carga_views.py
lines: 1702-1703
signature_hash: sha1:53713eb2710056e4ad984ea6ea9a83bfd4b07134
authored: true
---

# create_contrato_digital

**Módulo:** `api/views/carga_views.py` (líneas 1702-1703)

## Propósito

Alta de `ContratosDigitales` desde `ContratosDigitalesCreate` (`payload.model_dump()` directo a `ContratosDigitales.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_contrato_digital(request, payload: ContratosDigitalesCreate):
```

## Uso real

`POST /v1/api/contratos-digitales/` — response=`ContratosDigitalesOut`.

## Ver también

- [ContratosDigitales](../../../carga/models/ContratosDigitales.md)
