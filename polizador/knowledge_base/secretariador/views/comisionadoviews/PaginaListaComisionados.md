---
symbol: PaginaListaComisionados
kind: function
module: secretariador/views/comisionadoviews.py
lines: 57-60
signature_hash: sha1:0ba3e142f56f5660e0c335481f92244d2d243c18
authored: true
---

# PaginaListaComisionados

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 57-60)

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
