---
symbol: PaginaListaDirecciones
kind: function
module: personalizador/views/direccionviews.py
lines: 52-55
signature_hash: sha1:5552719d4d7619b303299fe483b5f750affccc4f
authored: true
---

# PaginaListaDirecciones

**Módulo:** `personalizador/views/direccionviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-direcciones.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaDirecciones(request):
```

## Uso real

`PaginaListaDirecciones` (`personalizador:lista-direcciones`).

## Ver también

- [Direccion](../../models/Direccion.md)
