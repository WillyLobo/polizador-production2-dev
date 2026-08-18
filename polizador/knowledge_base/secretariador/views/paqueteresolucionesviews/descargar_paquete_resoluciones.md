---
symbol: descargar_paquete_resoluciones
kind: function
module: secretariador/views/paqueteresolucionesviews.py
lines: 81-92
signature_hash: sha1:465e9f555c3eee5286c8ee738f0dce71b5c459da
authored: true
---

# descargar_paquete_resoluciones

**Módulo:** `secretariador/views/paqueteresolucionesviews.py` (líneas 81-92)

## Propósito

Redirige a la URL firmada/pública de un paquete puntual en GCS (`ano/mes/formato/indice` en la URL) — 404 si el formato es desconocido o el blob no existe en el bucket.

## Firma

```python
def descargar_paquete_resoluciones(request, ano, mes, formato, indice):
```

## Uso real

Enlazada desde cada fila de `PaginaListaPaquetesResoluciones`.

## Ver también

- [PaginaListaPaquetesResoluciones](PaginaListaPaquetesResoluciones.md)
