---
symbol: ManagementCommandRunDetailView
kind: class
module: core/views.py
lines: 180-183
signature_hash: sha1:65267d55fb765afdc862dcc748d3817b19131ed5
authored: true
---
# ManagementCommandRunDetailView

**Módulo:** `core/views.py` (líneas 180-183) · hereda de `SuperuserRequiredMixin, DetailView`

## Propósito

Ficha de detalle de una corrida puntual (sin lógica propia — `DetailView` simple). El template hace polling contra `ManagementCommandRunLogView` para mostrar el log en vivo mientras el comando sigue corriendo.

## Firma

```python
class ManagementCommandRunDetailView(SuperuserRequiredMixin, DetailView):
```

## Uso real

`ManagementCommandRunDetailView` (`management_command_run_detail`), destino tras lanzar un comando desde `ManagementCommandsView`.

## Ver también

- [ManagementCommandRunLogView](ManagementCommandRunLogView.md)