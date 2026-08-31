---
symbol: create_comisionado
kind: function
module: api/views/secretariador_views.py
lines: 486-487
signature_hash: sha1:8db6bdac503e472101d3411566b09f4e793886e6
authored: true
---
# create_comisionado

**Módulo:** `api/views/secretariador_views.py` (líneas 486-487)

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