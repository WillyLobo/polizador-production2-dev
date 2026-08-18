---
symbol: CrearApartadoCargo
kind: class
module: personalizador/views/apartadocargoviews.py
lines: 21-38
signature_hash: sha1:da4ef249cef33461ca08789b2026d976fc389ffc
authored: true
---

# CrearApartadoCargo

**Módulo:** `personalizador/views/apartadocargoviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de ApartadoCargo vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearApartadoCargo(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearApartadoCargo` (`personalizador:crear-apartadocargo`).

## Ver también

- [ApartadoCargo](../../models/ApartadoCargo.md)
