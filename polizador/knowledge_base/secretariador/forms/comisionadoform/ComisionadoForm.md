---
symbol: ComisionadoForm
kind: class
module: secretariador/forms/comisionadoform.py
lines: 6-49
signature_hash: sha1:4f2a031907f1bd7bb2ecfd3d0930c96b9760de78
authored: true
---

# ComisionadoForm

**Módulo:** `secretariador/forms/comisionadoform.py` (líneas 6-49) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` sobre `personalizador.Agente`, acotado a los campos relevantes para viáticos (nombres, sexo, oficina, DNI/CUIL, si es transitorio/gabinete) — la versión "liviana" de alta de Agente usada desde `secretariador`, en vez del `AgenteForm` completo de RRHH (~50 campos). Hereda `BaseFormMixin` (`core.mixins`), no visto en los forms de `carga`/`personalizador` (posiblemente agrega comportamiento común no cubierto en esta fase).

## Firma

```python
class ComisionadoForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearComisionado`/`UpdateComisionado` (`secretariador/views/comisionadoviews.py`).

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
