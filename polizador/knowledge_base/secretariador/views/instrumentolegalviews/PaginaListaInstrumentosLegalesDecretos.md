---
symbol: PaginaListaInstrumentosLegalesDecretos
kind: function
module: secretariador/views/instrumentolegalviews.py
lines: 184-187
signature_hash: sha1:9b9150fbb4922d91832de361380c2d140cfb7e3d
authored: true
---

# PaginaListaInstrumentosLegalesDecretos

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 184-187)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-decretos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `secretariador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaInstrumentosLegalesDecretos(request):
```

## Uso real

`PaginaListaInstrumentosLegalesDecretos` (`secretariador:lista-decretos`).

## Ver también

- [InstrumentosLegalesDecretos](../../models/InstrumentosLegalesDecretos.md)
