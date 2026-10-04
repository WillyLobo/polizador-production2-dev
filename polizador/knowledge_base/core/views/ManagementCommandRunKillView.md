---
symbol: ManagementCommandRunKillView
kind: class
module: core/views.py
lines: 201-205
signature_hash: sha1:b311a90bb6c6cf0689ebcbe25690d061621a01d3
authored: true
---
# ManagementCommandRunKillView

**Módulo:** `core/views.py` (líneas 201-205) · hereda de `SuperuserRequiredMixin, View`

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