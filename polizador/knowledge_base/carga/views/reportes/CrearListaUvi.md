---
symbol: CrearListaUvi
kind: class
module: carga/views/reportes.py
lines: 158-184
signature_hash: sha1:978a2cb724589a3a714b2cf0105d8642eada2243
authored: true
---
# CrearListaUvi

**Módulo:** `carga/views/reportes.py` (líneas 158-184) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Listado de cotizaciones `Uvi` en un rango de fechas — por defecto los últimos ~60 días hasta 10 días en el futuro; con `fecha_inicial`/`fecha_final` en querystring (formato `dd/mm/aaaa`), ese rango exacto.

## Firma

```python
class CrearListaUvi(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`CrearListaUvi` (`carga:lista-uvi`).

## Ver también

- [Uvi](../../models/Uvi.md)