---
symbol: BaseCommandRunForm
kind: class
module: core/forms.py
lines: 16-23
signature_hash: sha1:de46460501fd902929054c5536e50ad8f358d3a5
authored: true
---

# BaseCommandRunForm

**Módulo:** `core/forms.py` (líneas 16-23) · hereda de `forms.Form`

## Propósito

La base de **todos** los forms de `COMMAND_REGISTRY`: un `forms.Form` (no `ModelForm` —
no hay una instancia de modelo, es puro input de parámetros) con un único contrato,
`to_argv()`, que traduce los campos ya validados al `argv` real que recibe el subprocess
del management command. Deliberadamente manual (no se arma dinámicamente inspeccionando
`argparse` del comando): cada comando habilitado en el registry define su propia subclase
explícita, así que agregar un parámetro nuevo requiere tocar tanto el comando como su
form — el costo elegido a propósito para no exponer automáticamente cualquier flag nuevo
de un comando a la web sin revisión.

## Firma

```python
class BaseCommandRunForm(forms.Form):
```

## Uso real

Superclase de las 13 subclases de este módulo (una por comando en `COMMAND_REGISTRY`).

## Ver también

- [DryRunCheckApplyForm](DryRunCheckApplyForm.md)
