---
symbol: instrumentomemorandumwidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 191-195
signature_hash: sha1:055c2b63dbcd6f7ee3aed68768337522e6d57c37
authored: true
---

# instrumentomemorandumwidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 191-195) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir InstrumentosLegalesMemorandum (secretariador) vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Sin dependencia de otros campos.

## Firma

```python
class instrumentomemorandumwidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`LicenciaPermiso.licenciapermiso_instrumento_memorandum` en `LicenciaPermisoForm`.

## Ver también

- [LicenciaPermiso](../../models/LicenciaPermiso.md)
