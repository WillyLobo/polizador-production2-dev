---
symbol: DireccionForm
kind: class
module: personalizador/forms/direccionforms.py
lines: 5-29
signature_hash: sha1:67613d57c7cfe73a85e8e1bcbbdae0313fbf5000
authored: true
---

# DireccionForm

**Módulo:** `personalizador/forms/direccionforms.py` (líneas 5-29) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Direccion: puede colgar de `direccion_directorio` o `direccion_gerencia` (ambos widgets, sin dependencia entre sí — a diferencia de los widgets de `OficinaForm`, acá el usuario elige libremente cualquier combinación; la consistencia real la impone `Oficina.clean()`, no este form).

## Firma

```python
class DireccionForm(forms.ModelForm):
```

## Uso real

`CrearDireccion`/`UpdateDireccion`.

## Ver también

- [Direccion](../../models/Direccion.md)
