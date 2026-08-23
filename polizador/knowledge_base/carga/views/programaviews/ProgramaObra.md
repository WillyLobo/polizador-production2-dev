---
symbol: ProgramaObra
kind: class
module: carga/views/programaviews.py
lines: 50-54
signature_hash: sha1:f9ce1fca1b999c7adee4455390dae99fb09ff146
authored: true
---

# ProgramaObra

**Módulo:** `carga/views/programaviews.py` (líneas 50-54) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de Programa centrada en mostrar las Obras vinculadas a esta entrada del catálogo (sin lógica propia más allá del `DetailView` — el filtrado de Obras relacionadas lo resuelve el template, no una `get_context_data` propia).

## Firma

```python
class ProgramaObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`ProgramaObra` (`carga:programa-obra`), enlazada desde el listado de Programa.

## Ver también

- [Programa](../../models/Programa.md)
- [Obra](../../models/Obra.md)
