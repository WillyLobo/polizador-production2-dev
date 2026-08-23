---
symbol: CalendarioSemanal
kind: class
module: secretariador/views/reportesviews.py
lines: 315-331
signature_hash: sha1:8cfbb69e6adff4df21b1fdaef023cbf9540f7a7f
authored: true
---

# CalendarioSemanal

**Módulo:** `secretariador/views/reportesviews.py` (líneas 315-331) · hereda de `PermissionRequiredMixin, generic.TemplateView`

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
