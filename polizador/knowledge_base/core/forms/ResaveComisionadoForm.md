---
symbol: ResaveComisionadoForm
kind: class
module: core/forms.py
lines: 153-157
signature_hash: sha1:86669fc6637080d071d57b15d7cafd9f6f1c5caa
authored: true
---

# ResaveComisionadoForm

**Módulo:** `core/forms.py` (líneas 153-157) · hereda de `BaseCommandRunForm`

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
