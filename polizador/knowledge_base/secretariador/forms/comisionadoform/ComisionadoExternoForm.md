---
symbol: ComisionadoExternoForm
kind: class
module: secretariador/forms/comisionadoform.py
lines: 51-86
signature_hash: sha1:b2cec185eeff2063cdc86e2a18b265a547d3ad03
authored: true
---

# ComisionadoExternoForm

**Módulo:** `secretariador/forms/comisionadoform.py` (líneas 51-86) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` sobre `personalizador.ComisionadoExterno`: mismos campos de identidad que `ComisionadoForm` más `institucion_origen`, sin los campos de RRHH (oficina, tipo de personal) que no aplican a alguien externo.

## Firma

```python
class ComisionadoExternoForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearComisionadoExterno`/`UpdateComisionadoExterno`.

## Ver también

- [ComisionadoExterno](../../../personalizador/models/ComisionadoExterno.md)
