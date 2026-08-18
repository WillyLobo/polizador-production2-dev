---
symbol: PlanDeTrabajosItemForm
kind: class
module: carga/forms/plandetrabajositemforms.py
lines: 4-25
signature_hash: sha1:039e3155e9ea4a4673df5e36fc30fa65bc82b5f3
authored: true
---

# PlanDeTrabajosItemForm

**Módulo:** `carga/forms/plandetrabajositemforms.py` (líneas 4-25) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` para `PlanDeTrabajosItem` (nombre, orden, % de incidencia). Su único `clean()` normaliza `planitem_nombre` a mayúsculas — consistencia de datos cargados a mano por distintos usuarios.

## Firma

```python
class PlanDeTrabajosItemForm(forms.ModelForm):
```

## Uso real

Form base de `PlanDeTrabajosItemFormset` (dentro de `PlanDeTrabajosRubroForm`).

## Ver también

- [PlanDeTrabajosItem](../../models/PlanDeTrabajosItem.md)
