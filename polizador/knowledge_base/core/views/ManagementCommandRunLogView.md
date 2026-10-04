---
symbol: ManagementCommandRunLogView
kind: class
module: core/views.py
lines: 186-198
signature_hash: sha1:032b8c0d9119ccf9473f3199a90f9196742e9a22
authored: true
---
# ManagementCommandRunLogView

**Módulo:** `core/views.py` (líneas 186-198) · hereda de `SuperuserRequiredMixin, View`

## Propósito

Endpoint JSON de polling: devuelve el log **incremental** desde `offset` (`run.log[offset:]`, no el log completo cada vez) más el nuevo offset y el estado actual — el patrón estándar para mostrar la salida de un subprocess largo sin re-mandar todo el texto en cada poll.

## Firma

```python
class ManagementCommandRunLogView(SuperuserRequiredMixin, View):
```

## Uso real

Polling JS desde `comandos/detail.html` (template de `ManagementCommandRunDetailView`), cada N segundos mientras `status==RUNNING`.

## Ver también

- [ManagementCommandRunDetailView](ManagementCommandRunDetailView.md)