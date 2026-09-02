---
symbol: ManagementCommandRunLogView
kind: class
module: core/views.py
lines: 163-175
signature_hash: sha1:66efc27f94cb87240ce724d11ee58b41e9d90ed1
authored: true
---
# ManagementCommandRunLogView

**Módulo:** `core/views.py` (líneas 163-175) · hereda de `SuperuserRequiredMixin, View`

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