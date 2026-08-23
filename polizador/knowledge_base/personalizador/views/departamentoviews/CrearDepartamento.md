---
symbol: CrearDepartamento
kind: class
module: personalizador/views/departamentoviews.py
lines: 21-38
signature_hash: sha1:69a443223ac1a1970ee8ff0391e3c0799288237f
authored: true
---

# CrearDepartamento

**Módulo:** `personalizador/views/departamentoviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Departamento vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearDepartamento(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearDepartamento` (`personalizador:crear-departamento`).

## Ver también

- [Departamento](../../models/Departamento.md)
