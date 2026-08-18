---
symbol: create_financiamiento
kind: function
module: api/views/carga_views.py
lines: 1240-1241
signature_hash: sha1:96da67bdd3b10be5a70a199c99c14fd5fe8c425c
authored: true
---

# create_financiamiento

**Módulo:** `api/views/carga_views.py` (líneas 1240-1241)

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
