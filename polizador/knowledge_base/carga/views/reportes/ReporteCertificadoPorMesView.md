---
symbol: ReporteCertificadoPorMesView
kind: class
module: carga/views/reportes.py
lines: 21-69
signature_hash: sha1:416f61257d7f2b3e399f7aed5e99ba726449867f
authored: true
---

# ReporteCertificadoPorMesView

**Módulo:** `carga/views/reportes.py` (líneas 21-69) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Reporte de Certificados filtrado por mes/año (de `certificado_fecha` o `certificado_fecha_carga`, según el toggle `buscarPorFechaIngreso`), empresa y/u obra — todos opcionales vía querystring (`GET.getlist`). Sin ningún filtro, devuelve un queryset vacío en vez de listar todo (evita mandar la tabla completa por error). `get_context_data` arma las listas de años/meses disponibles a partir de `.dates()` sobre ambos campos de fecha, para poblar los combos de filtro solo con valores que existen de verdad.

## Firma

```python
class ReporteCertificadoPorMesView(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`ReporteCertificadoPorMesView` (`carga:crear-reporte-certificado`), enlazada desde el mega-menú "Reportes" del navbar.

## Ver también

- [Certificado](../../models/Certificado.md)
