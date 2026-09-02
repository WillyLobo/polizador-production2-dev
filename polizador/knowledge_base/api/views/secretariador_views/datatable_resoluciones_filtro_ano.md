---
symbol: datatable_resoluciones_filtro_ano
kind: function
module: api/views/secretariador_views.py
lines: 389-396
signature_hash: sha1:2b3f5c19909fb777584240bcae6ff25a33a1afbd
authored: true
---
# datatable_resoluciones_filtro_ano

**Módulo:** `api/views/secretariador_views.py` (líneas 389-396)

## Propósito

Años distintos (no vacíos) presentes en Resoluciones, para el `<select>` de filtro.

## Firma

```python
def datatable_resoluciones_filtro_ano(request):
```

## Uso real

`GET /v1/api/datatables/resoluciones/filtro-ano/`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)