---
symbol: create_prototipo
kind: function
module: api/views/carga_views.py
lines: 1167-1168
signature_hash: sha1:caacd16d5f917f82ac4bee45f4263e59090f97af
authored: true
---

# create_prototipo

**Módulo:** `api/views/carga_views.py` (líneas 1167-1168)

## Propósito

Alta de `Prototipo` desde `PrototipoCreate` (`payload.model_dump()` directo a `Prototipo.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_prototipo(request, payload: PrototipoCreate):
```

## Uso real

`POST /v1/api/prototipos/` — response=`PrototipoOut`.

## Ver también

- [Prototipo](../../../carga/models/Prototipo.md)
