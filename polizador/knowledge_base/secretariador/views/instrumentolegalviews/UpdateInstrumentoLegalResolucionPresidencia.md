---
symbol: UpdateInstrumentoLegalResolucionPresidencia
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 106-122
signature_hash: sha1:9d186960069a0948077f30e1830642b884416b68
authored: true
---

# UpdateInstrumentoLegalResolucionPresidencia

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 106-122) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de una Resolución de Presidencia. 
`get_context_data` agrega navegación "anterior/siguiente" por `pk - 1`/`pk + 1` — asume
que los IDs son correlativos y que cada vecino existe/es del mismo tipo, sin ningún
chequeo de que ese vecino sea realmente el instrumento "adyacente" en algún orden con
sentido (ej. por número/año). Es una forma barata de navegación secuencial que puede
saltar a un registro no relacionado si hay huecos en los IDs (por borrados).

## Firma

```python
class UpdateInstrumentoLegalResolucionPresidencia(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateInstrumentoLegalResolucionPresidencia` (`secretariador:update-resolucion-presidencia`).

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
