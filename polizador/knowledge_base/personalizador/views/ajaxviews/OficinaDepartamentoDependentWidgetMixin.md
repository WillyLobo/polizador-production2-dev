---
symbol: OficinaDepartamentoDependentWidgetMixin
kind: class
module: personalizador/views/ajaxviews.py
lines: 124-143
signature_hash: sha1:e942c59adc8da7161780df9f39b49d1203e0ed4d
authored: true
---

# OficinaDepartamentoDependentWidgetMixin

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 124-143) · hereda de `SmallCatalogWidgetMixin`

## Propósito

Mismo patrón, tres niveles de fallback: acota por Dirección, si no por Gerencia, si no por Directorio.

## Firma

```python
class OficinaDepartamentoDependentWidgetMixin(SmallCatalogWidgetMixin):
```

## Uso real

`class oficina_departamentowidget(OficinaDepartamentoDependentWidgetMixin, ...)`.

## Ver también

- [Oficina](../../models/Oficina.md)
- [oficina_departamentowidget](oficina_departamentowidget.md)
