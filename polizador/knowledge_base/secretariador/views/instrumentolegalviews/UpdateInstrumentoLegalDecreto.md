---
symbol: UpdateInstrumentoLegalDecreto
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 87-103
signature_hash: sha1:8e656cd31dd0c01f37ccd52343afc40ab1ffd30d
authored: true
---

# UpdateInstrumentoLegalDecreto

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 87-103) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un Decreto. 
`get_context_data` agrega navegación "anterior/siguiente" por `pk - 1`/`pk + 1` — asume
que los IDs son correlativos y que cada vecino existe/es del mismo tipo, sin ningún
chequeo de que ese vecino sea realmente el instrumento "adyacente" en algún orden con
sentido (ej. por número/año). Es una forma barata de navegación secuencial que puede
saltar a un registro no relacionado si hay huecos en los IDs (por borrados).

## Firma

```python
class UpdateInstrumentoLegalDecreto(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateInstrumentoLegalDecreto` (`secretariador:update-decreto`).

## Ver también

- [InstrumentosLegalesDecretos](../../models/InstrumentosLegalesDecretos.md)
