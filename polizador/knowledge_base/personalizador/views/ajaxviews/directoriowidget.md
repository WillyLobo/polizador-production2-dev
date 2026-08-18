---
symbol: directoriowidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 46-48
signature_hash: sha1:4e4639abc5dfd6f540055fbe59881dfac5762088
authored: true
---

# directoriowidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 46-48) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Directorio vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-directorio`).

## Firma

```python
class directoriowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Oficina.cargo_directorio`, `Gerencia.gerencia_directorio`, `Direccion.direccion_directorio`, `Departamento.departamento_directorio` en sus forms.

## Ver también

- [Directorio](../../models/Directorio.md)
