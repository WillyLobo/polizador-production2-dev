---
symbol: CalendarioSemanal
kind: class
module: secretariador/views/reportesviews.py
lines: 368-384
signature_hash: sha1:d7ca9482ae3ff2be826ec87a8e22cdb70345792e
authored: true
---
# CalendarioSemanal

**Módulo:** `secretariador/views/reportesviews.py` (líneas 368-384) · hereda de `PermissionRequiredMixin, generic.TemplateView`

## Propósito

Mismo patrón shell-de-filtros que `CrearReporteViaticosPorAgenteIndividual`, para la vista semanal general del calendario de comisiones — eventos vía `/v1/api/calendario/semanal/`.

## Firma

```python
class CalendarioSemanal(PermissionRequiredMixin, generic.TemplateView):
```

## Uso real

`CalendarioSemanal` (`secretariador:calendario-semanal`), enlazada desde el navbar ("Viáticos").

## Ver también

- [CalendarioAnual](CalendarioAnual.md)