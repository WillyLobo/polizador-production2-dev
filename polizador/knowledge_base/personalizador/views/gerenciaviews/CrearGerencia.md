---
symbol: CrearGerencia
kind: class
module: personalizador/views/gerenciaviews.py
lines: 21-38
signature_hash: sha1:c0e2ce998c66f020cfbe23f4978fcd58a9648ada
authored: true
---

# CrearGerencia

**Módulo:** `personalizador/views/gerenciaviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Gerencia vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearGerencia(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearGerencia` (`personalizador:crear-gerencia`).

## Ver también

- [Gerencia](../../models/Gerencia.md)
