---
symbol: create_localidad
kind: function
module: api/views/carga_views.py
lines: 621-622
signature_hash: sha1:cfb6c8eae29305faa647e231e13c48181df56ff1
authored: true
---

# create_localidad

**Módulo:** `api/views/carga_views.py` (líneas 621-622)

## Propósito

Alta de `Localidad` desde `LocalidadCreate` (`payload.model_dump()` directo a `Localidad.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_localidad(request, payload: LocalidadCreate):
```

## Uso real

`POST /v1/api/localidades/` — response=`LocalidadOut`.

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
