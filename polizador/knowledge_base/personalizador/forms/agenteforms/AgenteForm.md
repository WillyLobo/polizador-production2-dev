---
symbol: AgenteForm
kind: class
module: personalizador/forms/agenteforms.py
lines: 11-121
signature_hash: sha1:60ef8894cc84b6da5d88590ec81215eec7c684b9
authored: true
---

# AgenteForm

**Módulo:** `personalizador/forms/agenteforms.py` (líneas 11-121) · hereda de `forms.ModelForm`

## Propósito

El `ModelForm` más grande de `personalizador`: prácticamente todos los ~50 campos de Agente, cada catálogo relacionado con su propio widget select2 (género, títulos, categoría, denominación de cargo, oficina, apartado, CEIC, grupo, actividad específica) más `localidadwidget`/`provinciawidget` de `carga` para el domicilio. Sin `clean()` propio — ninguna validación cruzada a nivel form, todo lo que hay vive en `Agente.save()` (inferir abreviatura).

## Firma

```python
class AgenteForm(forms.ModelForm):
```

## Uso real

`CrearAgente`/`UpdateAgente` (`personalizador/views/agenteviews.py`).

## Ver también

- [Agente](../../models/Agente.md)
