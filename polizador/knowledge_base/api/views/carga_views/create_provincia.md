---
symbol: create_provincia
kind: function
module: api/views/carga_views.py
lines: 377-378
signature_hash: sha1:2c0ac5dab9aa13dfd3a0e74eecb5a5fd2cb07e1c
authored: true
---

# create_provincia

**Módulo:** `api/views/carga_views.py` (líneas 377-378)

## Propósito

Alta de `Provincia` desde `ProvinciaCreate` (`payload.model_dump()` directo a `Provincia.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_provincia(request, payload: ProvinciaCreate):
```

## Uso real

`POST /v1/api/provincias/` — response=`ProvinciaOut`.

## Ver también

- [Provincia](../../../carga/models/Provincia.md)
