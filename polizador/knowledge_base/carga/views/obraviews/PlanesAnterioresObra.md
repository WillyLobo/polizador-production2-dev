---
symbol: PlanesAnterioresObra
kind: class
module: carga/views/obraviews.py
lines: 133-146
signature_hash: sha1:313a9903fdfe282ff426df133c5ed46e6a80aec2
authored: true
---

# PlanesAnterioresObra

**Módulo:** `carga/views/obraviews.py` (líneas 133-146) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Lista los Planes de Trabajos de la Obra que no son el vigente (`Obra.plan_vigente()`) — el historial de reprogramaciones, ordenado del más reciente al más viejo.

## Firma

```python
class PlanesAnterioresObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`PlanesAnterioresObra` (`carga:planes-anteriores-obra`), enlazada desde `EstadoObra`.

## Ver también

- [PlanDeTrabajos](../../models/PlanDeTrabajos.md)
- [Obra](../../models/Obra.md)
