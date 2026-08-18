---
symbol: ManagementCommandRunKillView
kind: class
module: core/views.py
lines: 174-178
signature_hash: sha1:b1243792b9740c068fa95389f8fff0ab88f96c41
authored: true
---

# ManagementCommandRunKillView

**Módulo:** `core/views.py` (líneas 174-178) · hereda de `SuperuserRequiredMixin, View`

## Propósito

Mata el subprocess de una corrida en curso (`core.management_runner.kill_run()`) y vuelve al detalle — el botón "Detener" del panel de comandos.

## Firma

```python
class ManagementCommandRunKillView(SuperuserRequiredMixin, View):
```

## Uso real

`ManagementCommandRunKillView` (`management_command_run_kill`), enlazada desde `comandos/detail.html` mientras `status==RUNNING`.

## Ver también

- [ManagementCommandRunDetailView](ManagementCommandRunDetailView.md)
