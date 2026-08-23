---
symbol: OficinaGerenciaDependentWidgetMixin
kind: class
module: personalizador/views/ajaxviews.py
lines: 88-97
signature_hash: sha1:49eb8e7e1dc1b24b6e6c12399467c870ac6145aa
authored: true
---

# OficinaGerenciaDependentWidgetMixin

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 88-97) · hereda de `SmallCatalogWidgetMixin`

## Propósito

Acota las opciones de Gerencia al `Directorio` elegido en el campo hermano `cargo_directorio` de `OficinaForm` — evita que el usuario elija una combinación sin sentido en el select2 antes de guardar (la consistencia real la garantiza `Oficina.clean()`, esto es solo UX).

## Firma

```python
class OficinaGerenciaDependentWidgetMixin(SmallCatalogWidgetMixin):
```

## Uso real

`class oficina_gerenciawidget(OficinaGerenciaDependentWidgetMixin, ...)`.

## Ver también

- [Oficina](../../models/Oficina.md)
- [oficina_gerenciawidget](oficina_gerenciawidget.md)
