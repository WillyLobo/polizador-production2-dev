---
symbol: CrearTituloProfesional
kind: class
module: personalizador/views/tituloprofesionalviews.py
lines: 21-38
signature_hash: sha1:6a82b8339a14fba020ed03e81f4418b04c5d7a3e
authored: true
---

# CrearTituloProfesional

**Módulo:** `personalizador/views/tituloprofesionalviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de TituloProfesional vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearTituloProfesional(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearTituloProfesional` (`personalizador:crear-tituloprofesional`).

## Ver también

- [TituloProfesional](../../models/TituloProfesional.md)
