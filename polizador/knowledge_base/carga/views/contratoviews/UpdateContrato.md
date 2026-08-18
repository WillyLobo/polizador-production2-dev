---
symbol: UpdateContrato
kind: class
module: carga/views/contratoviews.py
lines: 34-44
signature_hash: sha1:b0ff8dbf22a77a3042cffd5ef00d82e7cc45028c
authored: true
---

# UpdateContrato

**Módulo:** `carga/views/contratoviews.py` (líneas 34-44) · hereda de `PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView`

## Propósito

Edición de Contrato + formset de montos. `get_success_url` (no `success_url` fijo) vuelve a la ficha de la Obra dueña — guardar montos de contrato dispara [recalcular_montos_obra](../../signals/recalcular_montos_obra.md), así que volver a la ficha de Obra muestra el efecto inmediato.

## Firma

```python
class UpdateContrato(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
```

## Uso real

`UpdateContrato` (`carga:update-contrato`).

## Ver también

- [Contrato](../../models/Contrato.md)
- [recalcular_montos_obra](../../signals/recalcular_montos_obra.md)
