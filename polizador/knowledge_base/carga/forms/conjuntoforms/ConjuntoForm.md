---
symbol: ConjuntoForm
kind: class
module: carga/forms/conjuntoforms.py
lines: 5-31
signature_hash: sha1:4c3a919571ca994e53a9ce37875a2bfc9a765cbd
authored: true
---

# ConjuntoForm

**Módulo:** `carga/forms/conjuntoforms.py` (líneas 5-31) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para ConjuntoLicitado: datos de resolución (mismo patrón `tipo/año/número/jurisdicción/acta` que Obra/Contrato) más `conjunto_subconjunto` para el sub-agrupamiento. Sin lógica propia.

## Firma

```python
class ConjuntoForm(forms.ModelForm):
```

## Uso real

`CrearConjunto`/`UpdateConjunto` (`carga/views/conjuntoviews.py`).

## Ver también

- [ConjuntoLicitado](../../models/ConjuntoLicitado.md)
