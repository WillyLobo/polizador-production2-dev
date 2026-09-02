---
symbol: InstrumentosLegalesDecretos
kind: class
module: secretariador/models.py
lines: 232-290
signature_hash: sha1:743f397647b16f832d789ab2e7f9be699dbcaaf0
authored: true
---
# InstrumentosLegalesDecretos

**Módulo:** `secretariador/models.py` (líneas 232-290) · hereda de `models.Model`

## Propósito

Un decreto (Nacional o Provincial). `instrumentolegaldecretos_establece_licencia_anual`/
`_establece_licencia_invierno` son flags que se tildan automáticamente (probablemente vía
OCR/import, no manualmente) cuando el decreto establece un período de Licencia Anual —
`personalizador.views.ajaxviews.InstrumentoDecretoLicenciaDependentWidgetMixin` los usa
para acotar el combo de decretos al cargar una Licencia/Permiso de ese tipo.
`get_absolute_url` es condicional: si el decreto ya tiene un `MontoViaticoDiario`
vinculado, va a la vista de edición de montos; si no, a la edición del decreto en sí —
un decreto "es" un decreto reglamentario de viáticos recién cuando se le cargan montos.

## Firma

```python
class InstrumentosLegalesDecretos(models.Model):
```

## Uso real

`MontoViaticoDiario.montoviaticodiario_decreto_reglamentario`; `personalizador.LicenciaPermiso.licenciapermiso_instrumento_decreto`.

## Ver también

- [MontoViaticoDiario](MontoViaticoDiario.md)