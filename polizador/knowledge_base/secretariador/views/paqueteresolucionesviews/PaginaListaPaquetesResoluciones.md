---
symbol: PaginaListaPaquetesResoluciones
kind: function
module: secretariador/views/paqueteresolucionesviews.py
lines: 72-76
signature_hash: sha1:e671f409e175de4a88642872b6fd2bb93b858f16
authored: true
---

# PaginaListaPaquetesResoluciones

**Módulo:** `secretariador/views/paqueteresolucionesviews.py` (líneas 72-76)

## Propósito

Lista los paquetes ZIP/PDF de resoluciones ya generados (por el management command mensual, ver CLAUDE.md sobre `empaquetar_resoluciones_mensual`), agrupados por mes.

## Firma

```python
def PaginaListaPaquetesResoluciones(request):
```

## Uso real

`PaginaListaPaquetesResoluciones` (`secretariador:lista-paquetes-resoluciones`), enlazada desde el navbar ("Herramientas").

## Ver también

- [_listar_meses](_listar_meses.md)
