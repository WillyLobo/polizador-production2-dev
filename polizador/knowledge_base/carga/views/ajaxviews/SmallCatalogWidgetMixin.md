---
symbol: SmallCatalogWidgetMixin
kind: class
module: carga/views/ajaxviews.py
lines: 34-41
signature_hash: sha1:8c350205c6d565d63eeaa4441b7eaba0db2ee57e
authored: true
---

# SmallCatalogWidgetMixin

**Módulo:** `carga/views/ajaxviews.py` (líneas 34-41)

## Propósito

Para catálogos con pocas filas (provincias, departamentos, municipios...): fuerza
`data-minimum-input-length=0` para que select2 muestre los primeros resultados apenas se
abre el combo, sin que el usuario tenga que escribir nada primero — no tendría sentido
pedir 2-3 caracteres mínimos en una tabla de 24 provincias.

## Firma

```python
class SmallCatalogWidgetMixin:
```

## Uso real

`class provinciawidget(SmallCatalogWidgetMixin, ...)`, junto con `departamentowidget`, `municipiowidget`, `aseguradorawidget`, `areawidget`, `programawidget`.

## Ver también

- [provinciawidget](provinciawidget.md)
