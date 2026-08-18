---
symbol: ConjuntoObra
kind: class
module: carga/views/conjuntoviews.py
lines: 49-53
signature_hash: sha1:982a6e0dcd7f467370cd06c959c342eeb76c5a59
authored: true
---

# ConjuntoObra

**Módulo:** `carga/views/conjuntoviews.py` (líneas 49-53) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de ConjuntoLicitado centrada en mostrar las Obras vinculadas a esta entrada del catálogo (sin lógica propia más allá del `DetailView` — el filtrado de Obras relacionadas lo resuelve el template, no una `get_context_data` propia).

## Firma

```python
class ConjuntoObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`ConjuntoObra` (`carga:conjunto-obra`), enlazada desde el listado de ConjuntoLicitado.

## Ver también

- [ConjuntoLicitado](../../models/ConjuntoLicitado.md)
- [Obra](../../models/Obra.md)
