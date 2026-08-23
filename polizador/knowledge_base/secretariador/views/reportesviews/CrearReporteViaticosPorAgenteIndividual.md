---
symbol: CrearReporteViaticosPorAgenteIndividual
kind: class
module: secretariador/views/reportesviews.py
lines: 293-312
signature_hash: sha1:9706331b0c9192d502ba6568cb44c0099b60e3b2
authored: true
---

# CrearReporteViaticosPorAgenteIndividual

**Módulo:** `secretariador/views/reportesviews.py` (líneas 293-312) · hereda de `PermissionRequiredMixin, generic.TemplateView`

## Propósito

Shell de filtros para el calendario de viáticos de un Agente puntual — los eventos del calendario en sí los trae FullCalendar vía AJAX desde `/v1/api/calendario/agente-individual/` (`api/views/secretariador_views.py`, fuera de `secretariador`); esta vista solo arma los valores iniciales (año, agente elegido) para que el template los use al inicializar el calendario.

## Firma

```python
class CrearReporteViaticosPorAgenteIndividual(PermissionRequiredMixin, generic.TemplateView):
```

## Uso real

`CrearReporteViaticosPorAgenteIndividual` (`secretariador:crear-reporte-viaticos-por-agente-individual`).

## Ver también

- [_anos_disponibles](_anos_disponibles.md)
