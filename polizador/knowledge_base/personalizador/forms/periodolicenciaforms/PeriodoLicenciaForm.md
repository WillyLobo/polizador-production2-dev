---
symbol: PeriodoLicenciaForm
kind: class
module: personalizador/forms/periodolicenciaforms.py
lines: 6-30
signature_hash: sha1:de687f8906bd7c24f808be5b96fa5d88c23e1c07
authored: true
---

# PeriodoLicenciaForm

**Módulo:** `personalizador/forms/periodolicenciaforms.py` (líneas 6-30) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para `PeriodoLicencia`: expone los 2 campos de `LOR_ANUAL`
(apertura/fecha límite de solicitud) y los 4 de turno de `LOR_INVIERNO` a la vez — el
partial (`partials/periodolicencia-form-partial.html`) es el que muestra/oculta el grupo
que corresponde según `periodolicencia_categoria` elegida, y precarga por JS
`15/12/<año>`/`31/03/<año+1>` para `LOR_ANUAL` cuando esos campos están vacíos (para
`LOR_INVIERNO` no hay fórmula fija, se cargan siempre a mano). Sin `clean()` propio: la
validación cruzada (qué campos son obligatorios según categoría, orden de los turnos)
vive en `PeriodoLicencia.clean()`.

## Firma

```python
class PeriodoLicenciaForm(forms.ModelForm):
```

## Uso real

`CrearPeriodoLicencia`/`UpdatePeriodoLicencia`.

## Ver también

- [PeriodoLicencia](../../models/PeriodoLicencia.md)
- [CrearPeriodoLicencia](../../views/periodolicenciaviews/CrearPeriodoLicencia.md)
