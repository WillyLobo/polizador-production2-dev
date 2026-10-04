---
symbol: Categoria
kind: class
module: personalizador/models.py
lines: 243-253
signature_hash: sha1:5aa8d74d4d02200f3e6d62b09e1dc46451d62cdf
authored: true
---

# Categoria

**Módulo:** `personalizador/models.py` (líneas 243-253) · hereda de `models.Model`

## Propósito

Catálogo de categorías de revista (código + nombre) — usado en `Agente.categoria`.

## Firma

```python
class Categoria(models.Model):
```

## Uso real

`CrearCategoria`/`UpdateCategoria` (`personalizador/views/categoriaviews.py`).

## Ver también

- [Agente](Agente.md)
