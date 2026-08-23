---
symbol: CrearMontoViaticoDiario
kind: class
module: secretariador/views/montoviaticodiarioviews.py
lines: 13-61
signature_hash: sha1:997277d8e2dbe7f80740c2ea52b0c9480d16d793
authored: true
---

# CrearMontoViaticoDiario

**Módulo:** `secretariador/views/montoviaticodiarioviews.py` (líneas 13-61) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un Decreto **con** su `MontoViaticoDiario` (formset de una sola fila, `max_num=1`) en el mismo paso — a diferencia de `instrumentolegalviews.CrearInstrumentoLegalDecreto` (solo el Decreto, sin montos). `get`/`post` manuales, mismo patrón que `incorporacionviews`.

## Firma

```python
class CrearMontoViaticoDiario(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearMontoViaticoDiario` (`secretariador:crear-montoviaticodiario`).

## Ver también

- [MontoViaticoDiario](../../models/MontoViaticoDiario.md)
- [InstrumentosLegalesDecretos](../../models/InstrumentosLegalesDecretos.md)
