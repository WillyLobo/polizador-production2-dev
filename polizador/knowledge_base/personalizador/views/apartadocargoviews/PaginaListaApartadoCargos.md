---
symbol: PaginaListaApartadoCargos
kind: function
module: personalizador/views/apartadocargoviews.py
lines: 52-55
signature_hash: sha1:71dabe00cfef5c706c65e0c4991b2e100f4e8117
authored: true
---

# PaginaListaApartadoCargos

**Módulo:** `personalizador/views/apartadocargoviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-apartadocargos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaApartadoCargos(request):
```

## Uso real

`PaginaListaApartadoCargos` (`personalizador:lista-apartadocargos`).

## Ver también

- [ApartadoCargo](../../models/ApartadoCargo.md)
