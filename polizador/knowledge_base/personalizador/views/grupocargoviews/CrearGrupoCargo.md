---
symbol: CrearGrupoCargo
kind: class
module: personalizador/views/grupocargoviews.py
lines: 21-38
signature_hash: sha1:9861d749563bf92b7b051c7edcfc04bfc599a141
authored: true
---

# CrearGrupoCargo

**Módulo:** `personalizador/views/grupocargoviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de GrupoCargo vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearGrupoCargo(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearGrupoCargo` (`personalizador:crear-grupocargo`).

## Ver también

- [GrupoCargo](../../models/GrupoCargo.md)
