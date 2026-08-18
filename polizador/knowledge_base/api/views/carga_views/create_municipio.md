---
symbol: create_municipio
kind: function
module: api/views/carga_views.py
lines: 538-539
signature_hash: sha1:038aeed5a0ea002471782181dabd1cd2b3a61ad4
authored: true
---

# create_municipio

**Módulo:** `api/views/carga_views.py` (líneas 538-539)

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
