---
symbol: instrumentodecretowidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 185-189
signature_hash: sha1:fcf5962d25762cb3d62c9fd5e06127249cd0f878
authored: true
---

# instrumentodecretowidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 185-189) · hereda de `InstrumentoDecretoLicenciaDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir InstrumentosLegalesDecretos (secretariador) vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Dependiente del tipo de licencia elegido (`InstrumentoDecretoLicenciaDependentWidgetMixin`).

## Firma

```python
class instrumentodecretowidget(InstrumentoDecretoLicenciaDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`LicenciaPermiso.licenciapermiso_instrumento_decreto` en `LicenciaPermisoForm`.

## Ver también

- [InstrumentoDecretoLicenciaDependentWidgetMixin](InstrumentoDecretoLicenciaDependentWidgetMixin.md)
