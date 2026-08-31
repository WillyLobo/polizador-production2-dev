---
symbol: datatable_agentes_detalle
kind: function
module: api/views/personalizador_views.py
lines: 754-778
signature_hash: sha1:45d58686408a831f445ade790d55c37838382920
authored: true
---
# datatable_agentes_detalle

**Módulo:** `api/views/personalizador_views.py` (líneas 754-778)

## Propósito

Expansión de fila del datatable de Agentes: renderiza `ajax_datatable/personalizador/agente/render_row_details.html` con el balance de licencias del año actual (`resumen_agente`) y saldos de cortes pendientes — mismos datos que `FichaAgente` (`personalizador/views/agenteviews.py`) muestra en su propia ficha, reusados acá para la vista rápida sin salir del listado.

## Firma

```python
def datatable_agentes_detalle(request, id: int):
```

## Uso real

`GET /v1/api/datatables/agentes/{id}/detalle/` — reemplaza el `with_detail=True` automático de `register_simple_datatable` porque necesita contexto extra (balance de licencias) que el helper genérico no arma.

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
- [FichaAgente](../../../personalizador/views/agenteviews/FichaAgente.md)