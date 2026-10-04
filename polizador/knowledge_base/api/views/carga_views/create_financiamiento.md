---
symbol: create_financiamiento
kind: function
module: api/views/carga_views.py
lines: 1241-1242
signature_hash: sha1:c33419c1ccc0b68d29574f59dc941d164889e10f
authored: true
---

# create_financiamiento

**Módulo:** `api/views/carga_views.py` (líneas 1241-1242)

## Propósito

Alta de `CertificadoFinanciamiento` desde `CertificadoFinanciamientoCreate` (`payload.model_dump()` directo a `CertificadoFinanciamiento.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_financiamiento(request, payload: CertificadoFinanciamientoCreate):
```

## Uso real

`POST /v1/api/financiamientos/` — response=`CertificadoFinanciamientoOut`.

## Ver también

- [CertificadoFinanciamiento](../../../carga/models/CertificadoFinanciamiento.md)
