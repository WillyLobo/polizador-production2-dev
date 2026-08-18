---
symbol: OficinaForm
kind: class
module: personalizador/forms/oficinaforms.py
lines: 8-24
signature_hash: sha1:4666789f6fb9e83a8d022d1c529124e916a0a7f4
authored: true
---

# OficinaForm

**Módulo:** `personalizador/forms/oficinaforms.py` (líneas 8-24) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` para Oficina, con los cuatro campos del árbol organizacional (cada nivel
condicionado al anterior vía los widgets `oficina_gerenciawidget`/`oficina_direccionwidget`/
`oficina_departamentowidget` — ver `personalizador/views/ajaxviews.py`). El form en sí no
tiene `clean()`: toda la validación/derivación de consistencia jerárquica vive en
`Oficina.clean()` (modelo), este form solo restringe las *opciones ofrecidas* en cada
select2 para guiar al usuario hacia una combinación válida antes de submitir.

## Firma

```python
class OficinaForm(forms.ModelForm):
```

## Uso real

`CrearOficina`/`UpdateOficina`.

## Ver también

- [Oficina](../../models/Oficina.md)
- [OficinaGerenciaDependentWidgetMixin](../ajaxviews/OficinaGerenciaDependentWidgetMixin.md)
