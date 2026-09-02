---
symbol: ComisionadoExternoForm
kind: class
module: secretariador/forms/comisionadoform.py
lines: 5-40
signature_hash: sha1:f4dd49fb6c3d5a979bea4467cdda8790d5cf3fbb
authored: true
---
# ComisionadoExternoForm

**Módulo:** `secretariador/forms/comisionadoform.py` (líneas 5-40) · hereda de `BaseFormMixin, forms.ModelForm`

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