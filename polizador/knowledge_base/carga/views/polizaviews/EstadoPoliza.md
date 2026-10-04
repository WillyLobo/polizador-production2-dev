---
symbol: EstadoPoliza
kind: class
module: carga/views/polizaviews.py
lines: 127-144
signature_hash: sha1:7d1fe90aa146151990acc3c7845338a42d1b4e4d
authored: true
---

# EstadoPoliza

**Módulo:** `carga/views/polizaviews.py` (líneas 127-144) · hereda de `PermissionRequiredMixin, generic.DetailView`

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
