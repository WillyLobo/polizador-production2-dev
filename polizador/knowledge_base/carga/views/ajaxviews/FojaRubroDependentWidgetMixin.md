---
symbol: FojaRubroDependentWidgetMixin
kind: class
module: carga/views/ajaxviews.py
lines: 105-122
signature_hash: sha1:879de436012553293add675800bd9045edb4ed4f
authored: true
---

# FojaRubroDependentWidgetMixin

**Módulo:** `carga/views/ajaxviews.py` (líneas 105-122)

## Propósito

Mismo mecanismo que `PlanDependentWidgetMixin` pero para `FojaDeMedicionForm`: acota
resultados AJAX a la Obra del `foja_rubro` elegido en el formulario. Lo usa
`certificadolegacywidget` para no ofrecer, como candidatos a vincular en una Foja legacy,
Certificados de *otras* Obras.

## Firma

```python
class FojaRubroDependentWidgetMixin:
```

## Uso real

`class certificadolegacywidget(FojaRubroDependentWidgetMixin, ...)`.

## Ver también

- [certificadolegacywidget](certificadolegacywidget.md)
- [FojaDeMedicion](../../models/FojaDeMedicion.md)
