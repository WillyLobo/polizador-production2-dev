---
symbol: LocalidadForm
kind: class
module: carga/forms/localidadforms.py
lines: 5-27
signature_hash: sha1:ff31b68b4673831e6bddda80995a780aa202e75c
authored: true
---

# LocalidadForm

**Módulo:** `carga/forms/localidadforms.py` (líneas 5-27) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Localidad, sin lógica propia. Incluye `id` editable (mismo motivo que `DepartamentoForm`: carga desde fuente externa con códigos propios) y el centroide lat/lon como `NumberInput` simples — no hay un widget de mapa, se cargan las coordenadas a mano.

## Firma

```python
class LocalidadForm(forms.ModelForm):
```

## Uso real

`CrearLocalidad`/`UpdateLocalidad`.

## Ver también

- [Localidad](../../models/Localidad.md)
- [departamentowidget](../../views/ajaxviews/departamentowidget.md)
