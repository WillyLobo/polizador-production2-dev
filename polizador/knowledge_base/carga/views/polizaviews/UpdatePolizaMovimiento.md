---
symbol: UpdatePolizaMovimiento
kind: class
module: carga/views/polizaviews.py
lines: 105-113
signature_hash: sha1:5ccc1563b971d4ce66a1a2b53512142ba86683b8
authored: true
---

# UpdatePolizaMovimiento

**Módulo:** `carga/views/polizaviews.py` (líneas 105-113) · hereda de `PermissionRequiredMixin, UserKwargsMixin, generic.UpdateView`

## Propósito

Edición de un `Poliza_Movimiento` puntual, fuera del formset de la Póliza. Exige
`carga.change_poliza_movimiento` y vuelve a la ficha de la Póliza.

## Firma

```python
class UpdatePolizaMovimiento(PermissionRequiredMixin, UserKwargsMixin, generic.UpdateView):
```

## Uso real

`carga:update-poliza-movimiento` (`crear/poliza/movimiento/<pk>/editar`).

## Ver también

- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)
- [CrearPolizaMovimiento](CrearPolizaMovimiento.md)
