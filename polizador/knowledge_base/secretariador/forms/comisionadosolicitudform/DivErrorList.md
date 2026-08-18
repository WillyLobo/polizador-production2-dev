---
symbol: DivErrorList
kind: class
module: secretariador/forms/comisionadosolicitudform.py
lines: 9-10
signature_hash: sha1:21d9c13870bb3e4d2dce69ed4cd0fa95d09a1163
authored: true
---

# DivErrorList

**Módulo:** `secretariador/forms/comisionadosolicitudform.py` (líneas 9-10) · hereda de `forms.utils.ErrorList`

## Propósito

Subclase mínima de `forms.utils.ErrorList` que solo cambia el `template_name` a `"generic/error_as_div.html"` — para que los errores de `ComisionadoSolicitudForm` se rendericen como `<div>`s en vez de la lista `<ul>` por defecto de Django (probablemente para encajar con el layout Bootstrap del formset).

## Firma

```python
class DivErrorList(forms.utils.ErrorList):
```

## Uso real

`ComisionadoSolicitudForm.__init__`: `self.error_class = DivErrorList`.

## Ver también

- [ComisionadoSolicitudForm](ComisionadoSolicitudForm.md)
