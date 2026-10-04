---
symbol: ImprimirPolizaMovimiento
kind: class
module: carga/views/polizaviews.py
lines: 147-163
signature_hash: sha1:eefc102e42cb5262723bd49a664cf9a1daa862d2
authored: true
---

# ImprimirPolizaMovimiento

**Módulo:** `carga/views/polizaviews.py` (líneas 147-163) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de impresión de un `Poliza_Movimiento` puntual (recibo/constancia del movimiento).

La nota impresa la firma **el usuario que la imprime**. `get_context_data()` busca su
`Agente` por `agente_usuario` y, como no todos los usuarios tienen ese vínculo cargado
todavía, si no lo encuentra lo busca por nombre y apellido (`iexact`). Después
[_firmante_organigrama](_firmante_organigrama.md) arma el bloque de firma (cargo, unidad y
gerencia) con los datos del organigrama.

## Firma

```python
class ImprimirPolizaMovimiento(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`ImprimirPolizaMovimiento` (`carga:imprimir-poliza-movimiento`).

## Ver también

- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)

- [_firmante_organigrama](_firmante_organigrama.md)
- [Agente](../../../personalizador/models/Agente.md)
