---
symbol: CrearConjunto
kind: class
module: carga/views/conjuntoviews.py
lines: 20-37
signature_hash: sha1:57d633150bbf6fb2b304f037b0df0bb2ac7474cb
authored: true
---

# CrearConjunto

**Módulo:** `carga/views/conjuntoviews.py` (líneas 20-37) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de ConjuntoLicitado vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`, `carga/views/ajaxviews.py`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir a otra página.

## Firma

```python
class CrearConjunto(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearConjunto` (`carga:crear-conjunto`).

## Ver también

- [ConjuntoLicitado](../../models/ConjuntoLicitado.md)
