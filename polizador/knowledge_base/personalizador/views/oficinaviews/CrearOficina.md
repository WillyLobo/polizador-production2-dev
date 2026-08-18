---
symbol: CrearOficina
kind: class
module: personalizador/views/oficinaviews.py
lines: 21-38
signature_hash: sha1:5b441e4fa2155a3226e2de276de974945b079231
authored: true
---

# CrearOficina

**Módulo:** `personalizador/views/oficinaviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Oficina vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearOficina(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearOficina` (`personalizador:crear-oficina`).

## Ver también

- [Oficina](../../models/Oficina.md)
