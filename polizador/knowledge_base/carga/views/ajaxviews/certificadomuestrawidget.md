---
symbol: certificadomuestrawidget
kind: class
module: carga/views/ajaxviews.py
lines: 250-259
signature_hash: sha1:8c203ff3341ba740281092e3fa80a4e066b7972f
authored: true
---

# certificadomuestrawidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 250-259) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Select2 de Certificados para elegir el "certificado de muestra" contra el que se
previsualiza una plantilla de texto de resolución. Busca por expediente o nombre de obra
(`icontains`), con hasta 10 resultados. A propósito **no** filtra por el alcance de la
plantilla: mientras se redacta, puede servir probar el texto contra cualquier certificado,
incluso uno de otro programa.

## Firma

```python
class certificadomuestrawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Widget del campo `certificado` de [CertificadoMuestraForm](../../forms/textoresolucionforms/CertificadoMuestraForm.md).

## Ver también

- [CertificadoMuestraForm](../../forms/textoresolucionforms/CertificadoMuestraForm.md)
- [TextoResolucionEditorMixin](../textoresolucionviews/TextoResolucionEditorMixin.md)
