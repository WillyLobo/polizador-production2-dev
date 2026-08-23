---
symbol: RegionObra
kind: class
module: carga/views/regionviews.py
lines: 50-54
signature_hash: sha1:ee5bab458f859215bf61304b79e0bf458536bdf4
authored: true
---

# RegionObra

**Módulo:** `carga/views/regionviews.py` (líneas 50-54) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de Region centrada en mostrar las Obras vinculadas a esta entrada del catálogo (sin lógica propia más allá del `DetailView` — el filtrado de Obras relacionadas lo resuelve el template, no una `get_context_data` propia).

## Firma

```python
class RegionObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`RegionObra` (`carga:region-obra`), enlazada desde el listado de Region.

## Ver también

- [Region](../../models/Region.md)
- [Obra](../../models/Obra.md)
