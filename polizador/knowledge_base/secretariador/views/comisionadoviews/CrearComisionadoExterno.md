---
symbol: CrearComisionadoExterno
kind: class
module: secretariador/views/comisionadoviews.py
lines: 27-44
signature_hash: sha1:71f1b482c7d573e5d0c1f81bf4bb2f6334ebe8f1
authored: true
---
# CrearComisionadoExterno

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 27-44) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

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