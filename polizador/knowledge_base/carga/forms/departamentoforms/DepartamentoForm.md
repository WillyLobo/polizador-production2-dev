---
symbol: DepartamentoForm
kind: class
module: carga/forms/departamentoforms.py
lines: 4-16
signature_hash: sha1:283dfe9b80cc2bd84c319bc81fa1ee28f235b492
authored: true
---

# DepartamentoForm

**Módulo:** `carga/forms/departamentoforms.py` (líneas 4-16) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Departamento, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets` (inputs Bootstrap, sin validación más allá de la del modelo). Incluye `id` como campo editable (no autoincremental — ver la página del modelo: se carga desde una fuente externa con sus propios códigos).

## Firma

```python
class DepartamentoForm(forms.ModelForm):
```

## Uso real

`CrearDepartamento/UpdateDepartamento` (`carga/views/`), tanto para alta como edición.

## Ver también

- [Departamento](../../models/Departamento.md)
