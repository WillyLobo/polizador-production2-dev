---
symbol: CrearEmpresa
kind: class
module: carga/views/empresaviews.py
lines: 21-38
signature_hash: sha1:47f0b65705fae0ecd7f03af23fd1ee733139f272
authored: true
---

# CrearEmpresa

**Módulo:** `carga/views/empresaviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Empresa vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`, `carga/views/ajaxviews.py`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir a otra página.

## Firma

```python
class CrearEmpresa(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearEmpresa` (`carga:crear-empresa`).

## Ver también

- [Empresa](../../models/Empresa.md)
