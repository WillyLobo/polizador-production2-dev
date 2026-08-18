---
symbol: UpdateInstrumentoLegalResolucionDirectorio
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 125-141
signature_hash: sha1:d58685998c0e761dfc199368c6d7db752ccba2df
authored: true
---

# UpdateInstrumentoLegalResolucionDirectorio

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 125-141) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de una Resolución de Directorio. 
`get_context_data` agrega navegación "anterior/siguiente" por `pk - 1`/`pk + 1` — asume
que los IDs son correlativos y que cada vecino existe/es del mismo tipo, sin ningún
chequeo de que ese vecino sea realmente el instrumento "adyacente" en algún orden con
sentido (ej. por número/año). Es una forma barata de navegación secuencial que puede
saltar a un registro no relacionado si hay huecos en los IDs (por borrados).

## Firma

```python
class UpdateInstrumentoLegalResolucionDirectorio(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateInstrumentoLegalResolucionDirectorio` (`secretariador:update-resolucion-directorio`).

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
