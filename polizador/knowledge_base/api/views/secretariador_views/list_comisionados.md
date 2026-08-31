---
symbol: list_comisionados
kind: function
module: api/views/secretariador_views.py
lines: 470-475
signature_hash: sha1:d1171409e4b7ffd8cf00e3c93ca75eb6f733f0a9
authored: true
---
# list_comisionados

**Módulo:** `api/views/secretariador_views.py` (líneas 470-475)

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