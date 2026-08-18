---
symbol: list_comisionados
kind: function
module: api/views/secretariador_views.py
lines: 463-468
signature_hash: sha1:f917f014fc80e0ea7a0d4eb7e52a4b4bd7deff9b
authored: true
---

# list_comisionados

**Módulo:** `api/views/secretariador_views.py` (líneas 463-468)

## Propósito

Listado paginado (`PerPagePagination`) de `Agente`, gateado por `require_model_perm(Agente)` (permiso `view_<modelo>`). Con `?q=` de texto libre (nombres/apellidos). "Comisionado" acá es el mismo `personalizador.Agente`, en su rol de viáticos — no un modelo propio de `secretariador`. Sin `update`.

## Firma

```python
def list_comisionados(request, q: str=''):
```

## Uso real

`GET /v1/api/comisionados/` — response=`List[AgenteOut]`.

## Ver también

- [Agente](../../../secretariador/models/Agente.md)
