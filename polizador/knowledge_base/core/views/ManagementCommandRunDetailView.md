---
symbol: ManagementCommandRunDetailView
kind: class
module: core/views.py
lines: 157-160
signature_hash: sha1:f0e9912690712d6a159a3d1e6d1654d96e1b00d0
authored: true
---
# ManagementCommandRunDetailView

**Módulo:** `core/views.py` (líneas 157-160) · hereda de `SuperuserRequiredMixin, DetailView`

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