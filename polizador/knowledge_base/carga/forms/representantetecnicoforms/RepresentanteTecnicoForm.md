---
symbol: RepresentanteTecnicoForm
kind: class
module: carga/forms/representantetecnicoforms.py
lines: 4-28
signature_hash: sha1:d6d83fe010f14fb85b695ff286e6a05262530657
authored: true
---

# RepresentanteTecnicoForm

**Módulo:** `carga/forms/representantetecnicoforms.py` (líneas 4-28) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para `personalizador.RepresentanteTecnico` (vive en `personalizador`, pero el CRUD web está en `carga` — ver `carga/views/representantetecnicoviews.py`). Sin lógica propia: datos de contacto + matrícula profesional.

## Firma

```python
class RepresentanteTecnicoForm(forms.ModelForm):
```

## Uso real

`CrearRepresentanteTecnico`/`UpdateRepresentanteTecnico`.

## Ver también

- [Obra](../../models/Obra.md) — `obra_representantetecnico` es el M2M que lo consume.
