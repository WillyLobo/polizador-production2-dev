---
symbol: CrearPrograma
kind: class
module: carga/views/programaviews.py
lines: 21-38
signature_hash: sha1:aa620788d66e8df3dca2fb262688a81b2eee9146
authored: true
---

# CrearPrograma

**Módulo:** `carga/views/programaviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Programa vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`, `carga/views/ajaxviews.py`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir a otra página.

## Firma

```python
class CrearPrograma(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearPrograma` (`carga:crear-programa`).

## Ver también

- [Programa](../../models/Programa.md)
