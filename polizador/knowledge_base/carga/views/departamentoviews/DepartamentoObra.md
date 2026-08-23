---
symbol: DepartamentoObra
kind: class
module: carga/views/departamentoviews.py
lines: 50-54
signature_hash: sha1:be7fddc03c253e61eabc53dc1c5347fc9b5973fb
authored: true
---

# DepartamentoObra

**Módulo:** `carga/views/departamentoviews.py` (líneas 50-54) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de Departamento centrada en mostrar las Obras vinculadas a esta entrada del catálogo (sin lógica propia más allá del `DetailView` — el filtrado de Obras relacionadas lo resuelve el template, no una `get_context_data` propia).

## Firma

```python
class DepartamentoObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`DepartamentoObra` (`carga:departamento-obra`), enlazada desde el listado de Departamento.

## Ver también

- [Departamento](../../models/Departamento.md)
- [Obra](../../models/Obra.md)
