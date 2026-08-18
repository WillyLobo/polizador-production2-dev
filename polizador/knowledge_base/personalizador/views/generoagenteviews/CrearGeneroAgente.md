---
symbol: CrearGeneroAgente
kind: class
module: personalizador/views/generoagenteviews.py
lines: 21-38
signature_hash: sha1:4288d8a38304b1b68ab63a48c77c7b61654de84f
authored: true
---

# CrearGeneroAgente

**Módulo:** `personalizador/views/generoagenteviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de GeneroAgente vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearGeneroAgente(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearGeneroAgente` (`personalizador:crear-generoagente`).

## Ver también

- [GeneroAgente](../../models/GeneroAgente.md)
