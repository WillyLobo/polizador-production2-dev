---
symbol: EstadoPoliza
kind: class
module: carga/views/polizaviews.py
lines: 61-78
signature_hash: sha1:6b82c0b2747fcb2c21ee4f2e0ff1c7f64a5e87bd
authored: true
---

# EstadoPoliza

**Módulo:** `carga/views/polizaviews.py` (líneas 61-78) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de estado de una Póliza. Guarda el `id` de la Póliza en la sesión (`request.session['poliza_id']`) — probablemente para que otra vista/flujo (ej. impresión) sepa cuál fue la última consultada sin pasarlo por URL.

## Firma

```python
class EstadoPoliza(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`EstadoPoliza` (`carga:estado-poliza`).

## Ver también

- [Poliza](../../models/Poliza.md)
