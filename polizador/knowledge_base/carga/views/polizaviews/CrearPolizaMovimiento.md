---
symbol: CrearPolizaMovimiento
kind: class
module: carga/views/polizaviews.py
lines: 76-101
signature_hash: sha1:ef5d2a6dc09061e0b099e54ad60ebaa6862a2502
authored: true
---

# CrearPolizaMovimiento

**Módulo:** `carga/views/polizaviews.py` (líneas 76-101) · hereda de `PermissionRequiredMixin, UserKwargsMixin, generic.CreateView`

## Propósito

Registra un movimiento (entrega de la póliza física a un receptor/área, con fecha) sobre una Póliza **ya existente**.
Antes sólo había el primer movimiento, cargado como formset dentro del alta de la Póliza.
Con `?poliza=<id>` precarga `poliza_movimiento_numero` (la FK a la Póliza). Usa
`UserKwargsMixin` porque `PolizaMovimientoForm` recibe al usuario. Exige
`carga.add_poliza_movimiento` y vuelve a la ficha de la Póliza.

## Firma

```python
class CrearPolizaMovimiento(PermissionRequiredMixin, UserKwargsMixin, generic.CreateView):
```

## Uso real

`carga:crear-poliza-movimiento` (`crear/poliza/movimiento/?poliza=<pk>`), desde la ficha de la Póliza.

## Ver también

- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)
- [UpdatePolizaMovimiento](UpdatePolizaMovimiento.md)
- [EliminarPolizaMovimiento](EliminarPolizaMovimiento.md)
