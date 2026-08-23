---
symbol: oficina_departamentowidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 145-147
signature_hash: sha1:4830b3346b1c030c626751bc95fb1473c8f50a9c
authored: true
---

# oficina_departamentowidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 145-147) · hereda de `OficinaDepartamentoDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Departamento (personalizador) vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Dependiente de Dirección/Gerencia/Directorio (`OficinaDepartamentoDependentWidgetMixin`). Con alta rápida (`personalizador:crear-departamento`).

## Firma

```python
class oficina_departamentowidget(OficinaDepartamentoDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Oficina.cargo_departamento` en `OficinaForm`.

## Ver también

- [OficinaDepartamentoDependentWidgetMixin](OficinaDepartamentoDependentWidgetMixin.md)
- [Oficina](../../models/Oficina.md)
