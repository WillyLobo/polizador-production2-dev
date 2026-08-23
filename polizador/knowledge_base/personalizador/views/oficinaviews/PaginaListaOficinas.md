---
symbol: PaginaListaOficinas
kind: function
module: personalizador/views/oficinaviews.py
lines: 52-55
signature_hash: sha1:6810c31e9994e15208cdbd9fdf8eb9cd869e133a
authored: true
---

# PaginaListaOficinas

**Módulo:** `personalizador/views/oficinaviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-oficinas.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaOficinas(request):
```

## Uso real

`PaginaListaOficinas` (`personalizador:lista-oficinas`).

## Ver también

- [Oficina](../../models/Oficina.md)
