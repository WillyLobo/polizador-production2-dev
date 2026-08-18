---
symbol: CrearSolicitudExterior
kind: class
module: secretariador/views/solicitud_exteriorviews.py
lines: 163-224
signature_hash: sha1:effad9389ef4a423ff908878fdf100adc1f368e5
authored: true
---

# CrearSolicitudExterior

**Módulo:** `secretariador/views/solicitud_exteriorviews.py` (líneas 163-224) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Solicitud (fuera del Chaco) — sobreescribe `get`/`post` en vez de apoyarse en `FormsetViewMixin` (a diferencia de `solicitudviews.CrearSolicitud`), manejando el formset de comisionados manualmente con la misma estructura get_context_data/form_valid/form_invalid que `CrearIncorporacion`.

## Firma

```python
class CrearSolicitudExterior(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearSolicitudExterior` (`secretariador:crear-solicitud-exterior`).

## Ver también

- [Solicitud](../../models/Solicitud.md)
- [CrearIncorporacion](../incorporacionviews/CrearIncorporacion.md) — mismo patrón de get/post manual.
