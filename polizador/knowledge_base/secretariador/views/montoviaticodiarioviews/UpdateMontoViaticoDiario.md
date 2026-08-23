---
symbol: UpdateMontoViaticoDiario
kind: class
module: secretariador/views/montoviaticodiarioviews.py
lines: 64-111
signature_hash: sha1:def1497674cf6e87778e8e81f124996cb978273f
authored: true
---

# UpdateMontoViaticoDiario

**Módulo:** `secretariador/views/montoviaticodiarioviews.py` (líneas 64-111) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un Decreto + su Monto de Viático Diario.

## Firma

```python
class UpdateMontoViaticoDiario(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateMontoViaticoDiario` (`secretariador:update-montoviaticodiario`) — destino de `InstrumentosLegalesDecretos.get_absolute_url()` cuando el decreto ya tiene montos cargados.

## Ver también

- [MontoViaticoDiario](../../models/MontoViaticoDiario.md)
