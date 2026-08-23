---
symbol: ActividadEspecificaForm
kind: class
module: personalizador/forms/actividadespecificaforms.py
lines: 4-16
signature_hash: sha1:8d019123e47bd55b6168e8505e7833a024200488
authored: true
---

# ActividadEspecificaForm

**Módulo:** `personalizador/forms/actividadespecificaforms.py` (líneas 4-16) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para ActividadEspecifica, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Código + nombre.

## Firma

```python
class ActividadEspecificaForm(forms.ModelForm):
```

## Uso real

`CrearActividadEspecifica/UpdateActividadEspecifica` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [ActividadEspecifica](../../models/ActividadEspecifica.md)
