---
symbol: tipolicenciapermisowidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 151-157
signature_hash: sha1:e353c0b484c019935c539e67c5b5e95fffff0fd7
authored: true
---

# tipolicenciapermisowidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 151-157) · hereda de `SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir TipoLicenciaPermiso vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico (~31 filas) pero **sin** `AddRelatedWidgetMixin` a propósito (ver el docstring): no tiene CRUD frecuente pensado desde acá, se carga vía management command.

## Firma

```python
class tipolicenciapermisowidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`LicenciaPermiso.licenciapermiso_tipo` en `LicenciaPermisoForm`.

## Ver también

- [TipoLicenciaPermiso](../../models/TipoLicenciaPermiso.md)
