---
symbol: EstadoObra
kind: class
module: carga/views/obraviews.py
lines: 117-130
signature_hash: sha1:19243b37b7b13bec33d23270d2a04e5f9347d8f7
authored: true
---

# EstadoObra

**Módulo:** `carga/views/obraviews.py` (líneas 117-130) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

La ficha principal de una Obra: todo el estado consolidado (contratos, montos, planes de trabajos, rubros, fojas, certificados) en una sola página, usando `_obra_estado_prefetch()` para traerlo todo sin N+1.

## Firma

```python
class EstadoObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`EstadoObra` (`carga:estado-obra`) — destino de la mayoría de los flujos de creación (Contrato, Plan de Trabajos, Foja...) una vez guardados.

## Ver también

- [_obra_estado_prefetch](_obra_estado_prefetch.md)
- [Obra](../../models/Obra.md)
