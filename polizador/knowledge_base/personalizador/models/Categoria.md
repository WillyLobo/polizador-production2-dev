---
symbol: Categoria
kind: class
module: personalizador/models.py
lines: 204-214
signature_hash: sha1:dc8751ebbd07aef9156cb2fa32d479dde71c1586
authored: true
---

# Categoria

**Módulo:** `personalizador/models.py` (líneas 204-214) · hereda de `models.Model`

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
