---
symbol: MunicipioObra
kind: class
module: carga/views/municipioviews.py
lines: 50-54
signature_hash: sha1:d7611d6b26fae7b1eabbdc81558b223f358ddd66
authored: true
---

# MunicipioObra

**Módulo:** `carga/views/municipioviews.py` (líneas 50-54) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de Municipio centrada en mostrar las Obras vinculadas a esta entrada del catálogo (sin lógica propia más allá del `DetailView` — el filtrado de Obras relacionadas lo resuelve el template, no una `get_context_data` propia).

## Firma

```python
class MunicipioObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`MunicipioObra` (`carga:municipio-obra`), enlazada desde el listado de Municipio.

## Ver también

- [Municipio](../../models/Municipio.md)
- [Obra](../../models/Obra.md)
