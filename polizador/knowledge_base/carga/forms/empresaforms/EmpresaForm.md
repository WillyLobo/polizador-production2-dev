---
symbol: EmpresaForm
kind: class
module: carga/forms/empresaforms.py
lines: 4-30
signature_hash: sha1:97f75cedc7288db3aaba6ce1817defb1524e06a1
authored: true
---

# EmpresaForm

**Módulo:** `carga/forms/empresaforms.py` (líneas 4-30) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Empresa, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets` (inputs Bootstrap, sin validación más allá de la del modelo). Todos los campos de contacto/identificación de la empresa contratista (CUIT, titular, dirección, dos correos) como inputs simples.

## Firma

```python
class EmpresaForm(forms.ModelForm):
```

## Uso real

`CrearEmpresa/UpdateEmpresa` (`carga/views/`), tanto para alta como edición.

## Ver también

- [Empresa](../../models/Empresa.md)
