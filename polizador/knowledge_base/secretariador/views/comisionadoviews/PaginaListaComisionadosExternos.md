---
symbol: PaginaListaComisionadosExternos
kind: function
module: secretariador/views/comisionadoviews.py
lines: 65-68
signature_hash: sha1:0bfe09c0d5a0ff5a93ebb09797fbe31bb584d0e7
authored: true
---
# PaginaListaComisionadosExternos

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 65-68)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-comisionados-externos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `secretariador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaComisionadosExternos(request):
```

## Uso real

`PaginaListaComisionadosExternos` (`secretariador:lista-comisionados-externos`).

## Ver también

- [ComisionadoExterno](../../../personalizador/models/ComisionadoExterno.md)