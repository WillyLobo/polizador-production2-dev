---
symbol: UpdateComisionado
kind: class
module: secretariador/views/comisionadoviews.py
lines: 32-38
signature_hash: sha1:8864b873d6878d61d141637130717404873aa158
authored: true
---

# UpdateComisionado

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 32-38) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un Agente vía el mismo `ComisionadoForm` acotado.

## Firma

```python
class UpdateComisionado(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateComisionado` (`secretariador:update-comisionado`).

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
