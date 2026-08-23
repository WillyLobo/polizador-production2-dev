---
symbol: tituloprofesionalmultiplewidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 18-20
signature_hash: sha1:d7531cf960d3b05456053a62ff49086fbd8018eb
authored: true
---

# tituloprofesionalmultiplewidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 18-20) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget select2 (`django-select2`) para elegir uno o más TituloProfesional vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-tituloprofesional`).

## Firma

```python
class tituloprofesionalmultiplewidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

`Agente.titulo_profesional` en `AgenteForm`.

## Ver también

- [TituloProfesional](../../models/TituloProfesional.md)
