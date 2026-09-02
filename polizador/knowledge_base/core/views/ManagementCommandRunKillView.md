---
symbol: ManagementCommandRunKillView
kind: class
module: core/views.py
lines: 178-182
signature_hash: sha1:4e68b14c4851fddab0009bf7a562947a5d05532e
authored: true
---
# ManagementCommandRunKillView

**Módulo:** `core/views.py` (líneas 178-182) · hereda de `SuperuserRequiredMixin, View`

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