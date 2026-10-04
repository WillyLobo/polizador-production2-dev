---
symbol: BaseBloqueTextoFormSet
kind: class
module: carga/forms/textoresolucionforms.py
lines: 153-163
signature_hash: sha1:cd477a51a3ee8c9eacf71611e8b4a2202cedf0b2
authored: true
---

# BaseBloqueTextoFormSet

**Módulo:** `carga/forms/textoresolucionforms.py` (líneas 153-163) · hereda de `forms.BaseFormSet`

## Propósito

Formset del texto resuelto. `bloques()` devuelve la lista `{clase, label, texto}` en el
mismo formato que los bloques de plantilla, que es la que se guarda en el snapshot
`certificado_texto_resolucion["bloques"]`. No borra ni reordena: la cantidad de bloques es
la que dio la plantilla.

## Firma

```python
class BaseBloqueTextoFormSet(forms.BaseFormSet):
```

## Uso real

```python
# carga/views/textoresolucionviews.py (editar_texto_resolucion_certificado)
"bloques": formset.bloques(),
```

## Ver también

- [BloqueTextoForm](BloqueTextoForm.md)
- [editar_texto_resolucion_certificado](../../views/textoresolucionviews/editar_texto_resolucion_certificado.md)
