---
symbol: BaseBloqueFormSet
kind: class
module: carga/forms/textoresolucionforms.py
lines: 80-100
signature_hash: sha1:a960a133b6a531a593ef4c5cf5323fe51f5a92fe
authored: true
---

# BaseBloqueFormSet

**Módulo:** `carga/forms/textoresolucionforms.py` (líneas 80-100) · hereda de `forms.BaseFormSet`

## Propósito

Formset de bloques de plantilla. `clean()` exige al menos un bloque no borrado.
`bloques_validos()` devuelve la lista `{clase, label, texto}` que se guarda en
`textoresolucion_bloques`: saltea los forms marcados `DELETE`, recorta `label` y vacía
`texto` para las clases sin texto. También se usa para la vista previa, así que lo que se
previsualiza es exactamente lo que se guardaría.

## Firma

```python
class BaseBloqueFormSet(forms.BaseFormSet):
```

## Uso real

```python
# carga/views/textoresolucionviews.py (TextoResolucionEditorMixin.post)
self.object.textoresolucion_bloques = formset.bloques_validos()
```

## Ver también

- [BloqueForm](BloqueForm.md)
- [TextoResolucionEditorMixin](../../views/textoresolucionviews/TextoResolucionEditorMixin.md)
