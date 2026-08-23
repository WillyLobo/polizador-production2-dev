---
symbol: contratomontowidget
kind: class
module: carga/views/ajaxviews.py
lines: 226-242
signature_hash: sha1:0bca1b660c1918e3b6ad53172f7437fd170a760b
authored: true
---

# contratomontowidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 226-242) · hereda de `PlanDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) ContratoMonto vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Dependiente del Plan elegido
(`PlanDependentWidgetMixin`): si el plan tiene un Contrato vinculado
(`trabajos_contrato`), ofrece solo los montos de *ese* Contrato; si no, ofrece los montos
de cualquier Contrato de la misma Obra.

## Firma

```python
class contratomontowidget(PlanDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`PlanDeTrabajosRubro.rubro_contratomonto` en `PlanDeTrabajosRubroForm`.

## Ver también

- [ContratoMonto](../../models/ContratoMonto.md)
- [PlanDependentWidgetMixin](PlanDependentWidgetMixin.md)
