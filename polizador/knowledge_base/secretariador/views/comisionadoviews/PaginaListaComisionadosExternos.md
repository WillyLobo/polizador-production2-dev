---
symbol: PaginaListaComisionadosExternos
kind: function
module: secretariador/views/comisionadoviews.py
lines: 101-104
signature_hash: sha1:591d0828876f5733f593d271d1c13e168c0ec1e2
authored: true
---

# PaginaListaComisionadosExternos

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 101-104)

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
