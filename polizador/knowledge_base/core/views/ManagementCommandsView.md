---
symbol: ManagementCommandsView
kind: class
module: core/views.py
lines: 144-177
signature_hash: sha1:eed12018f449a152094f80ba44d8492b03ae2bf2
authored: true
---
# ManagementCommandsView

**Módulo:** `core/views.py` (líneas 144-177) · hereda de `SuperuserRequiredMixin, TemplateView`

## Propósito

El panel `/administracion/comandos/`: lista el `COMMAND_REGISTRY` (whitelist de comandos
ejecutables desde la web, `core/management_commands_registry.py`), muestra el form del
comando seleccionado (`?command=<key>`), y en `post()` valida que no haya ya un comando
`RUNNING` (un solo comando a la vez — evita correr dos migraciones de datos superpuestas)
antes de delegar en `core.management_runner.start_run()` para lanzarlo como subprocess y
redirigir al detalle de esa corrida.

## Firma

```python
class ManagementCommandsView(SuperuserRequiredMixin, TemplateView):
```

## Uso real

`ManagementCommandsView` (`management_commands`), enlazada desde el navbar.

## Ver también

- [ManagementCommandRun](../models/ManagementCommandRun.md)
- [ManagementCommandRunDetailView](ManagementCommandRunDetailView.md)