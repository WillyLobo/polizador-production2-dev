---
symbol: create_direccion
kind: function
module: api/views/personalizador_views.py
lines: 83-84
signature_hash: sha1:649dd594f319346dc6aaac3df95acf58c83e2117
authored: true
---

# create_direccion

**Módulo:** `api/views/personalizador_views.py` (líneas 83-84)

## Propósito

Alta de `Direccion` desde `DireccionCreate` (`payload.model_dump()` directo a `Direccion.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_direccion(request, payload: DireccionCreate):
```

## Uso real

`POST /v1/api/direcciones/` — response=`DireccionOut`.

## Ver también

- [Direccion](../../../personalizador/models/Direccion.md)
