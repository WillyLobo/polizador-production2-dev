---
symbol: instrumentoresolucionwidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 159-163
signature_hash: sha1:8429a59e8707abd90134cbdef5bbe7b8c82ac90c
authored: true
---

# instrumentoresolucionwidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 159-163) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir InstrumentosLegalesResoluciones (secretariador) vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Sin dependencia de otros campos.

## Firma

```python
class instrumentoresolucionwidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`LicenciaPermiso.licenciapermiso_instrumento_resolucion` en `LicenciaPermisoForm`.

## Ver también

- [LicenciaPermiso](../../models/LicenciaPermiso.md)
