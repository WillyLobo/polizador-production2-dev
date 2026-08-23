---
symbol: ImprimirPolizaMovimiento
kind: class
module: carga/views/polizaviews.py
lines: 81-85
signature_hash: sha1:e9a3c80abfaea708fb4b501321a1c4ad48f08195
authored: true
---

# ImprimirPolizaMovimiento

**Módulo:** `carga/views/polizaviews.py` (líneas 81-85) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de impresión de un `Poliza_Movimiento` puntual (recibo/constancia del movimiento).

## Firma

```python
class ImprimirPolizaMovimiento(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`ImprimirPolizaMovimiento` (`carga:imprimir-poliza-movimiento`).

## Ver también

- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)
