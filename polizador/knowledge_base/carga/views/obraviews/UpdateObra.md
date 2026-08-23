---
symbol: UpdateObra
kind: class
module: carga/views/obraviews.py
lines: 97-114
signature_hash: sha1:58b578a636ecd03a6fef35a71fa95ade1519ede6
authored: true
---

# UpdateObra

**Módulo:** `carga/views/obraviews.py` (líneas 97-114) · hereda de `PermissionRequiredMixin, UserKwargsMixin, generic.UpdateView`

## Propósito

Edición de Obra. Agrega al contexto el Contrato vigente (y sus montos) y si hay más de uno, un flag `tiene_contratos_anteriores` para mostrar el link a `ContratosAnterioresObra`.

## Firma

```python
class UpdateObra(PermissionRequiredMixin, UserKwargsMixin, generic.UpdateView):
```

## Uso real

`UpdateObra` (`carga:update-obra`).

## Ver también

- [Obra](../../models/Obra.md)
- [ContratosAnterioresObra](ContratosAnterioresObra.md)
