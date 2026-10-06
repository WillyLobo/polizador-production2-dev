---
symbol: BloqueForm
kind: class
module: carga/forms/textoresolucionforms.py
lines: 42-77
signature_hash: sha1:0e72515d54761636acd63715ffde341de64c6619
authored: true
---

# BloqueForm

**Módulo:** `carga/forms/textoresolucionforms.py` (líneas 42-77) · hereda de `forms.Form`

## Propósito

Un bloque del cuerpo de una plantilla: `clase` (`CLASE_CHOICES`, en el orden habitual de una
resolución), `label` opcional (sólo para salirse de la numeración automática de artículos)
y `texto`, que es **fuente Jinja**.

`clean_texto()` compila el Jinja (`compilar_bloque`) sin renderizarlo, porque para eso hace
falta un certificado. Sin esta validación, un `{%` suelto rompería la ficha de todos los
certificados del alcance. `clean()` exige texto salvo para las clases de
`CLASES_SIN_TEXTO` (`resuelve`), cuya fórmula «EL PRESIDENTE ... RESUELVE:» es texto fijo
del organismo: el bloque marca dónde va, no qué dice.

## Firma

```python
class BloqueForm(forms.Form):
```

## Uso real

Form base de `BloqueFormSet = formset_factory(BloqueForm, formset=BaseBloqueFormSet, extra=0, can_delete=True)`.

## Ver también

- [BaseBloqueFormSet](BaseBloqueFormSet.md)
- [BloqueTextoForm](BloqueTextoForm.md) — el equivalente para el texto ya resuelto.
