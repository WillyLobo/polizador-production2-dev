---
symbol: FojaDeMedicionItemForm
kind: class
module: carga/forms/fojademedicionforms.py
lines: 138-162
signature_hash: sha1:414f10fa126980bb7e377359a5c81c0bd658338c
authored: true
---

# FojaDeMedicionItemForm

**Módulo:** `carga/forms/fojademedicionforms.py` (líneas 138-162) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` para `FojaDeMedicionItem`, con dos campos de solo lectura agregados (`fojaitem_pct_anterior`, `fojaitem_pct_acumulado`) puramente informativos — `disabled=True`, nunca se envían ni se usan para calcular nada; el acumulado real siempre lo calcula `FojaDeMedicionItem.save()`, este campo solo lo *muestra* en la grilla mientras se edita.

## Firma

```python
class FojaDeMedicionItemForm(forms.ModelForm):
```

## Uso real

Form base de `FojaDeMedicionItemFormset`/`build_foja_item_formset_class`.

## Ver también

- [FojaDeMedicionItem](../../models/FojaDeMedicionItem.md)
