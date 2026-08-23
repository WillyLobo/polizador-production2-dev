---
symbol: FojaDeMedicionItemForm
kind: class
module: carga/forms/fojademedicionforms.py
lines: 126-150
signature_hash: sha1:abd0212185d5139bfff6d24a7500fdbd23625c59
authored: true
---

# FojaDeMedicionItemForm

**Módulo:** `carga/forms/fojademedicionforms.py` (líneas 126-150) · hereda de `forms.ModelForm`

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
