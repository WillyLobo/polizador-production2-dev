---
symbol: CertificadoMuestraForm
kind: class
module: carga/forms/textoresolucionforms.py
lines: 106-118
signature_hash: sha1:d4d3216b6d127355abb92b171319651f795c7277
authored: true
---

# CertificadoMuestraForm

**Módulo:** `carga/forms/textoresolucionforms.py` (líneas 106-118) · hereda de `forms.Form`

## Propósito

Elige el certificado contra el que se previsualiza la plantilla. Hace falta porque la
plantilla se edita a nivel de alcance (programa, financiamiento, tipo), donde no hay ningún
certificado del que sacar valores. Opcional y nunca se guarda con la plantilla.

## Firma

```python
class CertificadoMuestraForm(forms.Form):
```

## Uso real

`muestra` en [TextoResolucionEditorMixin](../../views/textoresolucionviews/TextoResolucionEditorMixin.md), precargable con `?certificado=<id>`.

## Ver también

- [certificadomuestrawidget](../../views/ajaxviews/certificadomuestrawidget.md)
- [_previsualizar](../../views/textoresolucionviews/_previsualizar.md)
