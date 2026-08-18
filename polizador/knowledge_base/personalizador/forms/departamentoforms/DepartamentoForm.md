---
symbol: DepartamentoForm
kind: class
module: personalizador/forms/departamentoforms.py
lines: 5-31
signature_hash: sha1:00fa9ebdc567d002c819e187437499ea1e64a976
authored: true
---

# DepartamentoForm

**Módulo:** `personalizador/forms/departamentoforms.py` (líneas 5-31) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para `personalizador.Departamento` (nivel más específico del árbol organizacional — no confundir con `carga.forms.departamentoforms.DepartamentoForm`, geográfico): puede colgar de cualquiera de los tres niveles superiores, cada uno con su propio widget.

## Firma

```python
class DepartamentoForm(forms.ModelForm):
```

## Uso real

`CrearDepartamento`/`UpdateDepartamento` (`personalizador/views/departamentoviews.py`).

## Ver también

- [Departamento](../../models/Departamento.md)
