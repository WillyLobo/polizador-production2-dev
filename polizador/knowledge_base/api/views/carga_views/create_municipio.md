---
symbol: create_municipio
kind: function
module: api/views/carga_views.py
lines: 539-540
signature_hash: sha1:38f4a1ec376c465ae49af5713ad89fb8bf27b1bf
authored: true
---

# create_municipio

**Módulo:** `api/views/carga_views.py` (líneas 539-540)

## Propósito

Alta de `Municipio` desde `MunicipioCreate` (`payload.model_dump()` directo a `Municipio.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_municipio(request, payload: MunicipioCreate):
```

## Uso real

`POST /v1/api/municipios/` — response=`MunicipioOut`.

## Ver también

- [Municipio](../../../carga/models/Municipio.md)
