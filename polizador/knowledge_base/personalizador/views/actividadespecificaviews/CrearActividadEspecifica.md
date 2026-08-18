---
symbol: CrearActividadEspecifica
kind: class
module: personalizador/views/actividadespecificaviews.py
lines: 21-38
signature_hash: sha1:70ffaeed7ae3b49594b200a03ebbfadfae1fa41d
authored: true
---

# CrearActividadEspecifica

**Módulo:** `personalizador/views/actividadespecificaviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de ActividadEspecifica vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearActividadEspecifica(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearActividadEspecifica` (`personalizador:crear-actividadespecifica`).

## Ver también

- [ActividadEspecifica](../../models/ActividadEspecifica.md)
