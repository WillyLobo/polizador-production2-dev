---
symbol: create_organigrama
kind: function
module: api/views/secretariador_views.py
lines: 507-508
signature_hash: sha1:d7bba1eead1c8925385bbb0d5361d256421c8794
authored: true
---
# create_organigrama

**Módulo:** `api/views/secretariador_views.py` (líneas 507-508)

## Propósito

Alta de `Organigrama` desde `OrganigramaCreate` (`payload.model_dump()` directo a `Organigrama.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_organigrama(request, payload: OrganigramaCreate):
```

## Uso real

`POST /v1/api/organigramas/` — response=`OrganigramaOut`.

## Ver también

- [Organigrama](../../../secretariador/models/Organigrama.md)