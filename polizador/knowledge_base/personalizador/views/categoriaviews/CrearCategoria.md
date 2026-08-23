---
symbol: CrearCategoria
kind: class
module: personalizador/views/categoriaviews.py
lines: 21-38
signature_hash: sha1:db362fc9a01a52273c2a59b8d9192784cf4e3b29
authored: true
---

# CrearCategoria

**Módulo:** `personalizador/views/categoriaviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Categoria vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearCategoria(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearCategoria` (`personalizador:crear-categoria`).

## Ver también

- [Categoria](../../models/Categoria.md)
