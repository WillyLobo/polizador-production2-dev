---
symbol: create_organigrama
kind: function
module: api/views/secretariador_views.py
lines: 500-501
signature_hash: sha1:92f4c02a49701e5e58f5dd8b8c6d64aa95b605b4
authored: true
---

# create_organigrama

**Módulo:** `api/views/secretariador_views.py` (líneas 500-501)

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
