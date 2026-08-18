---
symbol: CrearComisionadoExterno
kind: class
module: secretariador/views/comisionadoviews.py
lines: 63-80
signature_hash: sha1:a22700b1ccab6d553e736957142da387ad84d97e
authored: true
---

# CrearComisionadoExterno

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 63-80) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un `ComisionadoExterno` (persona ajena al organismo) vía `PopupCreateMixin` — puede abrirse desde el modal de alta rápida de `ComisionadoExternoWidget`.

## Firma

```python
class CrearComisionadoExterno(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearComisionadoExterno` (`secretariador:crear-comisionado-externo`).

## Ver también

- [ComisionadoExterno](../../../personalizador/models/ComisionadoExterno.md)
