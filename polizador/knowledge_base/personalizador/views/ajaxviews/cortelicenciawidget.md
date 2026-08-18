---
symbol: cortelicenciawidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 211-212
signature_hash: sha1:26082e695ef48a683a75dd587746beaacee2619e
authored: true
---

# cortelicenciawidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 211-212) · hereda de `CorteLicenciaSaldoDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir CorteLicencia vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Dependiente del agente elegido (`CorteLicenciaSaldoDependentWidgetMixin`), solo ofrece cortes con saldo.

## Firma

```python
class cortelicenciawidget(CorteLicenciaSaldoDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`LicenciaPermiso.licenciapermiso_saldo_de_corte` en `LicenciaPermisoForm`.

## Ver también

- [CorteLicenciaSaldoDependentWidgetMixin](CorteLicenciaSaldoDependentWidgetMixin.md)
