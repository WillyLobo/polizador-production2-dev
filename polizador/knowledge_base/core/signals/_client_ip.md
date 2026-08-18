---
symbol: _client_ip
kind: function
module: core/signals.py
lines: 7-11
signature_hash: sha1:60152d7df8e6edcc8873e8640105c7c594509900
authored: true
---

# _client_ip

**Módulo:** `core/signals.py` (líneas 7-11)

## Propósito

Extrae la IP del cliente de la request, priorizando `X-Forwarded-For` (el primer valor de la lista, si el sitio está detrás de un proxy/load balancer) y cayendo a `REMOTE_ADDR` si no hay ese header.

## Firma

```python
def _client_ip(request):
```

## Uso real

`registrar_login` (mismo módulo, más abajo).

## Ver también

- [registrar_login](registrar_login.md)
