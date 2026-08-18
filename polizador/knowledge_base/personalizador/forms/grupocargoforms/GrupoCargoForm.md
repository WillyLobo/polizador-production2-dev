---
symbol: GrupoCargoForm
kind: class
module: personalizador/forms/grupocargoforms.py
lines: 4-14
signature_hash: sha1:b5b427368da7b02ed91efc4fba361691b16938fb
authored: true
---

# GrupoCargoForm

**Módulo:** `personalizador/forms/grupocargoforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para GrupoCargo, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Un solo campo: `grupo_numero`.

## Firma

```python
class GrupoCargoForm(forms.ModelForm):
```

## Uso real

`CrearGrupoCargo/UpdateGrupoCargo` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [GrupoCargo](../../models/GrupoCargo.md)
