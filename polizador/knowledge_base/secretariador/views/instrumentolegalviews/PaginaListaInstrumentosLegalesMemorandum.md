---
symbol: PaginaListaInstrumentosLegalesMemorandum
kind: function
module: secretariador/views/instrumentolegalviews.py
lines: 177-180
signature_hash: sha1:4b6001d615a919f07a73b4fba1c449fec8cb94aa
authored: true
---

# PaginaListaInstrumentosLegalesMemorandum

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 177-180)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-memorandum.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `secretariador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaInstrumentosLegalesMemorandum(request):
```

## Uso real

`PaginaListaInstrumentosLegalesMemorandum` (`secretariador:lista-memorandum`).

## Ver también

- [InstrumentosLegalesMemorandum](../../models/InstrumentosLegalesMemorandum.md)
