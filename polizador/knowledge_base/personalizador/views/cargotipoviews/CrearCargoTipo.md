---
symbol: CrearCargoTipo
kind: class
module: personalizador/views/cargotipoviews.py
lines: 21-38
signature_hash: sha1:1cfc06f639ca680ace6971949a39e6be3069898b
authored: true
---

# CrearCargoTipo

**Módulo:** `personalizador/views/cargotipoviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de CargoTipo vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearCargoTipo(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearCargoTipo` (`personalizador:crear-cargotipo`).

## Ver también

- [CargoTipo](../../models/CargoTipo.md)
