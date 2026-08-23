---
symbol: PlanDeTrabajosRubroForm
kind: class
module: carga/forms/plandetrabajosrubroforms.py
lines: 7-54
signature_hash: sha1:5f8475aba26029015ce6d0ee8829cfae1155b4e4
authored: true
---

# PlanDeTrabajosRubroForm

**Módulo:** `carga/forms/plandetrabajosrubroforms.py` (líneas 7-54) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` para `PlanDeTrabajosRubro`, con la lógica condicional del campo
"Número de Foja Inicial" (`rubro_foja_numero_inicial`): la vista decide vía
`pedir_foja_numero_inicial` (kwarg) si tiene sentido pedirlo, y el form lo deshabilita
(`disabled=True`, `required=False`) cuando no corresponde. `clean()` refuerza esa regla
del lado del dato: si el rubro tiene `rubro_anterior` (la numeración la determina la
cadena de reprogramación, no este campo) o si no correspondía preguntarlo, fuerza el
valor a `1` — para no dejar un valor espurio que el usuario haya llegado a tipear antes de
elegir un `rubro_anterior` en el mismo submit.

## Firma

```python
class PlanDeTrabajosRubroForm(forms.ModelForm):
```

## Uso real

`CrearPlanDeTrabajosRubro`/`UpdatePlanDeTrabajosRubro` (`carga/views/plandetrabajosrubroviews.py`).

## Ver también

- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
- [rubroanteriorwidget](../../views/ajaxviews/rubroanteriorwidget.md)
