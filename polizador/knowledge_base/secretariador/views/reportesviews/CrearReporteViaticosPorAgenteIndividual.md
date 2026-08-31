---
symbol: CrearReporteViaticosPorAgenteIndividual
kind: class
module: secretariador/views/reportesviews.py
lines: 346-365
signature_hash: sha1:9062f8b8cfd60f15f5571140223dcdb518fca1e8
authored: true
---
# CrearReporteViaticosPorAgenteIndividual

**Módulo:** `secretariador/views/reportesviews.py` (líneas 346-365) · hereda de `PermissionRequiredMixin, generic.TemplateView`

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