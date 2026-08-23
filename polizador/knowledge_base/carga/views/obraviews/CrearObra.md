---
symbol: CrearObra
kind: class
module: carga/views/obraviews.py
lines: 71-93
signature_hash: sha1:67a6dff6ccbcef507cda8658cbe89965af5379be
authored: true
---

# CrearObra

**Módulo:** `carga/views/obraviews.py` (líneas 71-93) · hereda de `PermissionRequiredMixin, UserKwargsMixin, generic.CreateView`

## Propósito

Alta de Obra vía `ObraForm`. Si el POST trae `next=contrato`, redirige después de guardar directo al alta de Contrato con `obra` precargado por querystring — flujo pensado para no tener que ir a buscar la Obra recién creada desde el listado.

## Firma

```python
class CrearObra(PermissionRequiredMixin, UserKwargsMixin, generic.CreateView):
```

## Uso real

`CrearObra` (`carga:crear-obra`), enlazada desde el navbar ("Obras > Nueva Obra").

## Ver también

- [Obra](../../models/Obra.md)
- [CrearContrato](CrearContrato.md)
