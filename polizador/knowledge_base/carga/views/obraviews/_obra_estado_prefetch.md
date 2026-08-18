---
symbol: _obra_estado_prefetch
kind: function
module: carga/views/obraviews.py
lines: 24-60
signature_hash: sha1:07b55b26c9ef4dbc72cc9377069cd3ba8ef6a5ff
authored: true
---

# _obra_estado_prefetch

**Módulo:** `carga/views/obraviews.py` (líneas 24-60)

## Propósito

Lista de `prefetch_related`/`Prefetch` que arma de una sola vez todo lo que
`estado-obra.html` recorre (contratos con sus montos y documentos, certificados con su
rubro, todos los planes de trabajos con sus rubros/items/etapas/fojas) — evita el N+1 que
tendría esa ficha si cada relación se resolviera fila por fila al renderizar el template.
Factorizada en función aparte porque `EstadoObra.get_queryset()` la necesita dos veces:
una para la Obra pedida y otra (recursiva) para su `obra_madre`, que en la ficha también
muestra su propio detalle anidado.

## Firma

```python
def _obra_estado_prefetch():
```

## Uso real

`EstadoObra.get_queryset()` (mismo módulo, más abajo).

## Ver también

- [EstadoObra](EstadoObra.md)
- [Obra](../../models/Obra.md)
