---
symbol: GerenciaForm
kind: class
module: personalizador/forms/gerenciaforms.py
lines: 5-27
signature_hash: sha1:adba074ec4e01bd84eae30342acd9ee9643479e4
authored: true
---

# GerenciaForm

**Módulo:** `personalizador/forms/gerenciaforms.py` (líneas 5-27) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Gerencia: agrega `gerencia_directorio` (`directoriowidget`) sobre los mismos campos que `DirectorioForm`. Sin lógica propia — la consistencia jerárquica no se valida acá (Gerencia no tiene una regla de derivación como Oficina).

## Firma

```python
class GerenciaForm(forms.ModelForm):
```

## Uso real

`CrearGerencia`/`UpdateGerencia`.

## Ver también

- [Gerencia](../../models/Gerencia.md)
- [Directorio](../../models/Directorio.md)
