---
symbol: EmpresaObra
kind: class
module: carga/views/empresaviews.py
lines: 51-55
signature_hash: sha1:550d89598acb0a45c037d15d2f77929fe49d4552
authored: true
---

# EmpresaObra

**Módulo:** `carga/views/empresaviews.py` (líneas 51-55) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de Empresa centrada en mostrar las Obras vinculadas a esta entrada del catálogo (sin lógica propia más allá del `DetailView` — el filtrado de Obras relacionadas lo resuelve el template, no una `get_context_data` propia).

## Firma

```python
class EmpresaObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`EmpresaObra` (`carga:empresa-obra`), enlazada desde el listado de Empresa.

## Ver también

- [Empresa](../../models/Empresa.md)
- [Obra](../../models/Obra.md)
