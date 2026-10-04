---
symbol: BloqueTextoForm
kind: class
module: carga/forms/textoresolucionforms.py
lines: 136-150
signature_hash: sha1:21c48099212411cdb8d788bfa5767628b8e8fb53
authored: true
---

# BloqueTextoForm

**Módulo:** `carga/forms/textoresolucionforms.py` (líneas 136-150) · hereda de `forms.Form`

## Propósito

Un bloque del texto **ya resuelto** de un certificado concreto. A diferencia de
[BloqueForm](BloqueForm.md), el texto es final y no se compila como Jinja: unas llaves
sueltas en una resolución son llaves, no un error. `clase` y `label` van ocultos y no se
pueden cambiar, porque la estructura del documento la fija la plantilla. Acá sólo se retoca
la redacción.

## Firma

```python
class BloqueTextoForm(forms.Form):
```

## Uso real

Form base de `BloqueTextoFormSet` (`extra=0`), usado por [editar_texto_resolucion_certificado](../../views/textoresolucionviews/editar_texto_resolucion_certificado.md).

## Ver también

- [BaseBloqueTextoFormSet](BaseBloqueTextoFormSet.md)
