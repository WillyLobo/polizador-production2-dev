---
symbol: LocalidadObra
kind: class
module: carga/views/localidadviews.py
lines: 50-54
signature_hash: sha1:f672f8e13239e3481fdd31a2a13b8b0aceb505db
authored: true
---

# LocalidadObra

**Módulo:** `carga/views/localidadviews.py` (líneas 50-54) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de Localidad centrada en mostrar las Obras vinculadas a esta entrada del catálogo (sin lógica propia más allá del `DetailView` — el filtrado de Obras relacionadas lo resuelve el template, no una `get_context_data` propia).

## Firma

```python
class LocalidadObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`LocalidadObra` (`carga:localidad-obra`), enlazada desde el listado de Localidad.

## Ver también

- [Localidad](../../models/Localidad.md)
- [Obra](../../models/Obra.md)
