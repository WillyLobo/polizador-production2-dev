---
symbol: CrearListaUvi
kind: class
module: carga/views/reportes.py
lines: 164-190
signature_hash: sha1:d4842f1beb5d3fdc5b5fac6c9ee4a0a6e9f77f42
authored: true
---
# CrearListaUvi

**Módulo:** `carga/views/reportes.py` (líneas 164-190) · hereda de `PermissionRequiredMixin, generic.ListView`

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