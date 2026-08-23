---
symbol: PaginaListaVehiculos
kind: function
module: secretariador/views/vehiculoviews.py
lines: 50-53
signature_hash: sha1:f78803052449625b56a0c2f31ef76d6cc2ba5338
authored: true
---

# PaginaListaVehiculos

**Módulo:** `secretariador/views/vehiculoviews.py` (líneas 50-53)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-vehiculos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `secretariador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaVehiculos(request):
```

## Uso real

`PaginaListaVehiculos` (`secretariador:lista-vehiculos`).

## Ver también

- [Vehiculo](../../models/Vehiculo.md)
