---
symbol: PaginaListaComisionados
kind: function
module: secretariador/views/comisionadoviews.py
lines: 21-24
signature_hash: sha1:3fd4c92c7631f574c5557e1a0a244a28aa1d383b
authored: true
---
# PaginaListaComisionados

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 21-24)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-comisionados.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `secretariador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaComisionados(request):
```

## Uso real

`PaginaListaComisionados` (`secretariador:lista-comisionados`).

## Ver también

_(sin referencias cruzadas)_