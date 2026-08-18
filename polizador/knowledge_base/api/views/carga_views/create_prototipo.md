---
symbol: create_prototipo
kind: function
module: api/views/carga_views.py
lines: 1166-1167
signature_hash: sha1:adbf52e89a47b57ed91adf036ba88dbc9fe77e38
authored: true
---

# create_prototipo

**Módulo:** `api/views/carga_views.py` (líneas 1166-1167)

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
