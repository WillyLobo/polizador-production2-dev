---
symbol: PaginaListaDenominacionCargos
kind: function
module: personalizador/views/denominacioncargoviews.py
lines: 52-55
signature_hash: sha1:41360e74e597d94b565687c84c33203ab0a28bb6
authored: true
---

# PaginaListaDenominacionCargos

**Módulo:** `personalizador/views/denominacioncargoviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-denominacioncargos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaDenominacionCargos(request):
```

## Uso real

`PaginaListaDenominacionCargos` (`personalizador:lista-denominacioncargos`).

## Ver también

- [DenominacionCargo](../../models/DenominacionCargo.md)
