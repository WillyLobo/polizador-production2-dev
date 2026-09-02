---
symbol: ResaveComisionadoForm
kind: class
module: core/forms.py
lines: 160-164
signature_hash: sha1:43ed9c15d7b1a38c4df38d0bfdfe8c1fcfbcb3ce
authored: true
---
# ResaveComisionadoForm

**Módulo:** `core/forms.py` (líneas 160-164) · hereda de `BaseCommandRunForm`

## Propósito

`resave_comisionado` no toma argumentos: `to_argv()` devuelve `[]`.

## Firma

```python
class ResaveComisionadoForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["resave_comisionado"]["form"]`.

## Ver también

- [ComisionadoSolicitud](../../../secretariador/models/ComisionadoSolicitud.md)