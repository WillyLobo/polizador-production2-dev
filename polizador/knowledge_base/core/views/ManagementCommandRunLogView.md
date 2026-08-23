---
symbol: ManagementCommandRunLogView
kind: class
module: core/views.py
lines: 159-171
signature_hash: sha1:9bf0d172bfd4bb64fc32bebd741e8a3e0450a1e3
authored: true
---

# ManagementCommandRunLogView

**Módulo:** `core/views.py` (líneas 159-171) · hereda de `SuperuserRequiredMixin, View`

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
