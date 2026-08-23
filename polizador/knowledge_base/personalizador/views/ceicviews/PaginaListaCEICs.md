---
symbol: PaginaListaCEICs
kind: function
module: personalizador/views/ceicviews.py
lines: 52-55
signature_hash: sha1:ce25736cc91ea35b6760da2ebbd3bcd8c385ecf2
authored: true
---

# PaginaListaCEICs

**Módulo:** `personalizador/views/ceicviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-ceics.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaCEICs(request):
```

## Uso real

`PaginaListaCEICs` (`personalizador:lista-ceics`).

## Ver también

- [CEIC](../../models/CEIC.md)
