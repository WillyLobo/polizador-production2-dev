---
symbol: CalendarioAnual
kind: class
module: secretariador/views/reportesviews.py
lines: 334-354
signature_hash: sha1:a64558be9f7e0de256633ab4b0632ac79fd12aec
authored: true
---

# CalendarioAnual

**Módulo:** `secretariador/views/reportesviews.py` (líneas 334-354) · hereda de `PermissionRequiredMixin, generic.TemplateView`

## Propósito

Mismo patrón, vista anual — eventos vía `/v1/api/calendario/anual/`. Sin año explícito en la URL, arranca en la semana actual; con `?ano=`, arranca el 1° de enero de ese año.

## Firma

```python
class CalendarioAnual(PermissionRequiredMixin, generic.TemplateView):
```

## Uso real

`CalendarioAnual` (`secretariador:calendario-anual`), enlazada desde el navbar.

## Ver también

- [_anos_disponibles](_anos_disponibles.md)
- [CalendarioSemanal](CalendarioSemanal.md)
