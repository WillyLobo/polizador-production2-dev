---
symbol: RepresentanteTecnicoObra
kind: class
module: carga/views/representantetecnicoviews.py
lines: 50-54
signature_hash: sha1:dc5a44eb5c787061c8059cdff4feccc59f4b03ba
authored: true
---

# RepresentanteTecnicoObra

**Módulo:** `carga/views/representantetecnicoviews.py` (líneas 50-54) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de RepresentanteTecnico centrada en mostrar las Obras vinculadas a esta entrada del catálogo (sin lógica propia más allá del `DetailView` — el filtrado de Obras relacionadas lo resuelve el template, no una `get_context_data` propia).

## Firma

```python
class RepresentanteTecnicoObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`RepresentanteTecnicoObra` (`carga:representantetecnico-obra`), enlazada desde el listado de RepresentanteTecnico.

## Ver también

- [RepresentanteTecnico](../../models/RepresentanteTecnico.md)
- [Obra](../../models/Obra.md)
