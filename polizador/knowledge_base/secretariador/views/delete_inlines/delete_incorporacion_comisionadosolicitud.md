---
symbol: delete_incorporacion_comisionadosolicitud
kind: function
module: secretariador/views/delete_inlines.py
lines: 32-45
signature_hash: sha1:97a65e9dc3f48364a500c8281698eb37f4c161bc
authored: true
---

# delete_incorporacion_comisionadosolicitud

**Módulo:** `secretariador/views/delete_inlines.py` (líneas 32-45)

## Propósito

Misma función y mismo bug que `delete_comisionadosolicitud` (`comisionado` sin asignar en la rama `except`), pero para comisionados de una `Incorporacion` en vez de una `Solicitud` directa.

## Firma

```python
def delete_incorporacion_comisionadosolicitud(request, pk):
```

## Uso real

Enlazada desde `UpdateIncorporacion`.

## Ver también

- [delete_comisionadosolicitud](delete_comisionadosolicitud.md)
- [Incorporacion](../../models/Incorporacion.md)
