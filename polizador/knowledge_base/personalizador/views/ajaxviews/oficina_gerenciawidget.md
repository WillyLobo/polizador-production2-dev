---
symbol: oficina_gerenciawidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 99-101
signature_hash: sha1:59068f908176379e818e46d3defdee16bee85294
authored: true
---

# oficina_gerenciawidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 99-101) · hereda de `OficinaGerenciaDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Gerencia vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Dependiente del Directorio elegido (`OficinaGerenciaDependentWidgetMixin`). Con alta rápida (`personalizador:crear-gerencia`).

## Firma

```python
class oficina_gerenciawidget(OficinaGerenciaDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Oficina.cargo_gerencia` en `OficinaForm`.

## Ver también

- [OficinaGerenciaDependentWidgetMixin](OficinaGerenciaDependentWidgetMixin.md)
- [Oficina](../../models/Oficina.md)
