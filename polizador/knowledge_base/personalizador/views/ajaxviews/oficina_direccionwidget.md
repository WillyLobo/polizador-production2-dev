---
symbol: oficina_direccionwidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 120-122
signature_hash: sha1:d6a823a856dcad64b3c3f374753574d80278b283
authored: true
---

# oficina_direccionwidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 120-122) · hereda de `OficinaDireccionDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Direccion vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Dependiente de Gerencia/Directorio (`OficinaDireccionDependentWidgetMixin`). Con alta rápida (`personalizador:crear-direccion`).

## Firma

```python
class oficina_direccionwidget(OficinaDireccionDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Oficina.cargo_direccion` en `OficinaForm`.

## Ver también

- [OficinaDireccionDependentWidgetMixin](OficinaDireccionDependentWidgetMixin.md)
- [Oficina](../../models/Oficina.md)
