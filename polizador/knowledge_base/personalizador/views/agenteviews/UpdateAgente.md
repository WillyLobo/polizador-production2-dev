---
symbol: UpdateAgente
kind: class
module: personalizador/views/agenteviews.py
lines: 44-50
signature_hash: sha1:72ec50d6c959af350860e501922ccda0b73e6304
authored: true
---

# UpdateAgente

**Módulo:** `personalizador/views/agenteviews.py` (líneas 44-50) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Agente. Sin lógica propia más allá del `ModelForm` estándar.

## Firma

```python
class UpdateAgente(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateAgente` (`personalizador:update-agente`).

## Ver también

- [Agente](../../models/Agente.md)
