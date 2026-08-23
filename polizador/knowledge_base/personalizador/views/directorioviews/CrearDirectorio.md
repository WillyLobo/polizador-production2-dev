---
symbol: CrearDirectorio
kind: class
module: personalizador/views/directorioviews.py
lines: 21-38
signature_hash: sha1:439ad9facb591ea1c3ab8c7359c765bc0b17bfd1
authored: true
---

# CrearDirectorio

**Módulo:** `personalizador/views/directorioviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Directorio vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearDirectorio(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearDirectorio` (`personalizador:crear-directorio`).

## Ver también

- [Directorio](../../models/Directorio.md)
