---
symbol: CrearReporteObraView
kind: class
module: carga/views/reportes.py
lines: 71-155
signature_hash: sha1:165f2da1dfbb15f9c67c592db7d17f7834dedc32
authored: true
---

# CrearReporteObraView

**Módulo:** `carga/views/reportes.py` (líneas 71-155) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Reporte de Obras con filtros combinables (localidad, empresa, programa, rubro certificado, financiamiento, y un filtro de % de avance con comparador =/</> vía `tipodefiltro`). También sin filtros devuelve vacío. `get_context_data` calcula a mano (no en la query) el acumulado en pesos/UVI y el saldo de cada Obra listada, iterando sus Certificados — con muchas Obras en el resultado esto es N+1 real, aunque mitigado por el `prefetch_related('certificado_set')` del queryset.

## Firma

```python
class CrearReporteObraView(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`CrearReporteObraView` (`carga:crear-reporte-obra`), enlazada desde el mega-menú "Reportes".

## Ver también

- [Obra](../../models/Obra.md)
