---
symbol: PaginaListaInstrumentosLegalesResoluciones
kind: function
module: secretariador/views/instrumentolegalviews.py
lines: 191-194
signature_hash: sha1:53fe8102a6f1ad0bbf20f9278a39c308cfb4c21c
authored: true
---

# PaginaListaInstrumentosLegalesResoluciones

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 191-194)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-resoluciones.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `secretariador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaInstrumentosLegalesResoluciones(request):
```

## Uso real

`PaginaListaInstrumentosLegalesResoluciones` (`secretariador:lista-resoluciones`) — lista tanto Presidencia como Directorio (mismo modelo).

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
