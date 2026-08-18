---
symbol: redirect_solicitudes
kind: function
module: secretariador/views/redirects.py
lines: 17-20
signature_hash: sha1:add141266209a7588fe314759db9ab78cf19f375
authored: true
---

# redirect_solicitudes

**Módulo:** `secretariador/views/redirects.py` (líneas 17-20)

## Propósito

Mismo patrón, para Solicitudes — el destino de "Viáticos > Nueva Solicitud" en el navbar, que a su vez enlaza a `CrearSolicitud` o `CrearSolicitudExterior` según corresponda.

## Firma

```python
def redirect_solicitudes(request):
```

## Uso real

Enlazada desde el navbar.

## Ver también

- [redirect_decretos](redirect_decretos.md)
