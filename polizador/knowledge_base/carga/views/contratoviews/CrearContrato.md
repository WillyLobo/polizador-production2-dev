---
symbol: CrearContrato
kind: class
module: carga/views/contratoviews.py
lines: 12-31
signature_hash: sha1:c7029e09a59c11f390f6b187181eca7a795e5971
authored: true
---

# CrearContrato

**Módulo:** `carga/views/contratoviews.py` (líneas 12-31) · hereda de `PermissionRequiredMixin, FormsetViewMixin, generic.CreateView`

## Propósito

Alta de Contrato junto con su formset inline de `ContratoMonto` (`FormsetViewMixin`). Si viene `?obra=<id>`, precarga la Obra destino.

## Firma

```python
class CrearContrato(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
```

## Uso real

`CrearContrato` (`carga:crear-contrato`), enlazada desde `CrearObra` (flujo `?next=contrato`) y desde la ficha de Obra.

## Ver también

- [Contrato](../../models/Contrato.md)
- [ContratoMonto](../../models/ContratoMonto.md)
- [CrearObra](../obraviews/CrearObra.md)
