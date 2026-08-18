---
symbol: CrearListaUvi
kind: class
module: carga/views/reportes.py
lines: 158-185
signature_hash: sha1:3d7f457f3f047ccdbd45598c8f5793333f94efa8
authored: true
---

# CrearListaUvi

**Módulo:** `carga/views/reportes.py` (líneas 158-185) · hereda de `PermissionRequiredMixin, generic.ListView`

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
