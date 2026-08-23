---
symbol: check_resolucion
kind: function
module: secretariador/views/ajaxviews.py
lines: 20-31
signature_hash: sha1:6219505d7a7e205eb9d75cde230a0bffafc8d96b
authored: true
---

# check_resolucion

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 20-31)

## Propósito

Endpoint AJAX que chequea si ya existe una `InstrumentosLegalesResoluciones` con el número+año dados (`{results: true/false}`) — probablemente usado en el form de carga de resolución para avisar de un posible duplicado mientras el usuario tipea, antes de submitir.

## Firma

```python
def check_resolucion(request):
```

## Uso real

`$HOST/viaticos/ajax/check_resolucion/?instrumentolegalresoluciones_numero=...&instrumentolegalresoluciones_ano=...` (ver el comentario de uso en el propio código).

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
