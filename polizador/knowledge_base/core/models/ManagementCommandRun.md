---
symbol: ManagementCommandRun
kind: class
module: core/models.py
lines: 6-75
signature_hash: sha1:6169d32daf55a89f9461efb1cb8dbfb4bd0e3222
authored: true
---

# ManagementCommandRun

**Módulo:** `core/models.py` (líneas 6-75) · hereda de `models.Model`

## Propósito

El registro de una ejecución de management command disparada desde
`/administracion/comandos/` (ver [ManagementCommandsView](../views/ManagementCommandsView.md)).
`command` es la **clave dentro de `COMMAND_REGISTRY`**, no el nombre real del management
command — el whitelist (`core/management_commands_registry.py`) es la única fuente de
verdad sobre qué se puede ejecutar desde la web, así que este campo por sí solo no basta
para saber qué corrió; siempre se resuelve contra el registry (ver `label`, property).

`duration`/`duration_display` calculan el tiempo transcurrido; mientras `status==RUNNING`,
`duration` lo calcula contra "ahora" en cada acceso (no un valor fijo — crece en cada
request mientras el comando sigue corriendo, ver el comentario del código).

## Firma

```python
class ManagementCommandRun(models.Model):
```

## Uso real

`core.management_runner.start_run()` crea la instancia; `ManagementCommandRunDetailView`/`ManagementCommandRunLogView` la leen para mostrar progreso en vivo (polling).

## Ver también

- [ManagementCommandsView](../views/ManagementCommandsView.md)
- [ManagementCommandRunLogView](../views/ManagementCommandRunLogView.md)
