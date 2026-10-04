---
symbol: CrearReporteObraView
kind: class
module: carga/views/reportes.py
lines: 72-161
signature_hash: sha1:347a4f5bc02bef20ed7a7fdd830c4be8ee57fab5
authored: true
---

# CrearReporteObraView

**Módulo:** `carga/views/reportes.py` (líneas 72-161) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Reporte de Obras con filtros combinables (localidad, empresa, programa, inspector, rubro certificado, financiamiento, y un filtro de % de avance con comparador =/</> vía `tipodefiltro`). También sin filtros devuelve vacío. `get_context_data` calcula a mano (no en la query) el acumulado en pesos/UVI y el saldo de cada Obra listada, iterando sus Certificados — con muchas Obras en el resultado esto es N+1 real, aunque mitigado por el `prefetch_related('certificado_set')` del queryset.

## Firma

```python
class CrearReporteObraView(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`CrearReporteObraView` (`carga:crear-reporte-obra`), enlazada desde el mega-menú "Reportes".

## Ver también

- [Obra](../../models/Obra.md)

- [Agente](../../../personalizador/models/Agente.md) — filtro por inspector (`obra_inspector`).
