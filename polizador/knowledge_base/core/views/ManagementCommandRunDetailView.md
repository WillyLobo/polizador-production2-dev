---
symbol: ManagementCommandRunDetailView
kind: class
module: core/views.py
lines: 153-156
signature_hash: sha1:4342f0eb017f98866993608271c8d8f13dae9b2c
authored: true
---

# ManagementCommandRunDetailView

**Módulo:** `core/views.py` (líneas 153-156) · hereda de `SuperuserRequiredMixin, DetailView`

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
