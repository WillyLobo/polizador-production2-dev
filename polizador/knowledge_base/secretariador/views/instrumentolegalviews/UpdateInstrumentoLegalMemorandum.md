---
symbol: UpdateInstrumentoLegalMemorandum
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 68-84
signature_hash: sha1:9f58e064c90cc0bd2cb44b430743062d8956631a
authored: true
---

# UpdateInstrumentoLegalMemorandum

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 68-84) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un Memorandum. 
`get_context_data` agrega navegación "anterior/siguiente" por `pk - 1`/`pk + 1` — asume
que los IDs son correlativos y que cada vecino existe/es del mismo tipo, sin ningún
chequeo de que ese vecino sea realmente el instrumento "adyacente" en algún orden con
sentido (ej. por número/año). Es una forma barata de navegación secuencial que puede
saltar a un registro no relacionado si hay huecos en los IDs (por borrados).

## Firma

```python
class UpdateInstrumentoLegalMemorandum(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateInstrumentoLegalMemorandum` (`secretariador:update-memorandum`).

## Ver también

- [InstrumentosLegalesMemorandum](../../models/InstrumentosLegalesMemorandum.md)
