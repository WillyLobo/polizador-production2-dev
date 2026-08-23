---
symbol: CrearIncorporacion
kind: class
module: secretariador/views/incorporacionviews.py
lines: 146-207
signature_hash: sha1:4b6bfe3136537484447d2ed89e9f15d27494ea56
authored: true
---

# CrearIncorporacion

**Módulo:** `secretariador/views/incorporacionviews.py` (líneas 146-207) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Incorporación junto con su formset de `ComisionadoSolicitud` propio (`ComisionadoIncorporacionFormset`), con `get`/`post` manuales (mismo patrón que `CrearSolicitudExterior`) en vez de `FormsetViewMixin`.

## Firma

```python
class CrearIncorporacion(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearIncorporacion` (`secretariador:crear-incorporacion`).

## Ver también

- [Incorporacion](../../models/Incorporacion.md)
- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)
