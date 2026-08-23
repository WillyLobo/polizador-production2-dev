---
symbol: PaginaListaPeriodoLicencias
kind: function
module: personalizador/views/periodolicenciaviews.py
lines: 52-55
signature_hash: sha1:d4950613c2a4431cbf726f8c07073f25b4fc6083
authored: true
---

# PaginaListaPeriodoLicencias

**Módulo:** `personalizador/views/periodolicenciaviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla
(`Lista-periodolicencias.html`), sin pasarle datos. La tabla se llena después vía AJAX
contra `register_simple_datatable(router, PeriodoLicencia, "periodolicencias", ...)`
(`api/views/personalizador_views.py`), con expansión de fila (`detailUrl`) hacia
[_periodolicencia_datatable_row](../../../api/views/personalizador_views/_periodolicencia_datatable_row.md)
para listar las solicitudes hechas contra cada período.

## Firma

```python
def PaginaListaPeriodoLicencias(request):
```

## Uso real

`PaginaListaPeriodoLicencias` (`personalizador:lista-periodolicencias`), enlazada desde el
navbar ("Períodos de Licencia").

## Ver también

- [PeriodoLicencia](../../models/PeriodoLicencia.md)
