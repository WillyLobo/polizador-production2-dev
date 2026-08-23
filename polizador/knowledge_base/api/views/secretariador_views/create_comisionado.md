---
symbol: create_comisionado
kind: function
module: api/views/secretariador_views.py
lines: 479-480
signature_hash: sha1:de77de85b8736b2005aa5d425a93e26d1e06235b
authored: true
---

# create_comisionado

**Módulo:** `api/views/secretariador_views.py` (líneas 479-480)

## Propósito

Alta de `Agente` desde `AgenteCreate` (`payload.model_dump()` directo a `Agente.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_comisionado(request, payload: ComisionadoCreate):
```

## Uso real

`POST /v1/api/comisionados/` — response=`AgenteOut`.

## Ver también

- [Agente](../../../secretariador/models/Agente.md)
