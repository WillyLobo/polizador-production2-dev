---
symbol: ParrafoForm
kind: class
module: secretariador/forms/textoactuacionform.py
lines: 4-6
signature_hash: sha1:163978a6f6b59f19ad308c7182e98292be7802eb
authored: true
---

# ParrafoForm

**Módulo:** `secretariador/forms/textoactuacionform.py` (líneas 4-6) · hereda de `forms.Form`

## Propósito

Un único campo de texto libre (`Textarea`), representando un considerando editable ("parrafo_uno"..."N") en el flujo de revisión de texto antes de generar el `.docx`.

## Firma

```python
class ParrafoForm(forms.Form):
```

## Uso real

`ParrafoFormSet = forms.formset_factory(ParrafoForm, extra=0)` (mismo módulo, sin subclase propia — no aparece como símbolo aparte), usado en `textoactuacionviews.revisar_texto_actuacion`.

## Ver también

- [revisar_texto_actuacion](../../views/textoactuacionviews/revisar_texto_actuacion.md)
