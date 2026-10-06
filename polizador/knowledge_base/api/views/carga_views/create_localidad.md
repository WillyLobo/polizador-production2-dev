---
symbol: create_localidad
kind: function
module: api/views/carga_views.py
lines: 622-623
signature_hash: sha1:7cfe8b9569f4c53b70d2a5d858ce5d7577bfcc46
authored: true
---

# create_localidad

**Módulo:** `api/views/carga_views.py` (líneas 622-623)

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
