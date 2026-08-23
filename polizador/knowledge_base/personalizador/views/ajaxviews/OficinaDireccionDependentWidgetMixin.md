---
symbol: OficinaDireccionDependentWidgetMixin
kind: class
module: personalizador/views/ajaxviews.py
lines: 103-118
signature_hash: sha1:cc86921334e67810c6940323684fb03244d74d09
authored: true
---

# OficinaDireccionDependentWidgetMixin

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 103-118) · hereda de `SmallCatalogWidgetMixin`

## Propósito

Mismo patrón que `OficinaGerenciaDependentWidgetMixin` para Dirección: acota por Gerencia elegida, o por Directorio si no hay Gerencia elegida (dos niveles de fallback, siguiendo la misma jerarquía que `Oficina.clean()` deriva).

## Firma

```python
class OficinaDireccionDependentWidgetMixin(SmallCatalogWidgetMixin):
```

## Uso real

`class oficina_direccionwidget(OficinaDireccionDependentWidgetMixin, ...)`.

## Ver también

- [Oficina](../../models/Oficina.md)
- [oficina_direccionwidget](oficina_direccionwidget.md)
