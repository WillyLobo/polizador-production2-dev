---
symbol: CrearContratoDigital
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 17-40
signature_hash: sha1:129754133cbb71cf5632b35404c9e9eb66f1957d
authored: true
---

# CrearContratoDigital

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 17-40) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un documento PDF adjunto a un Contrato (`ContratosDigitales`). Si viene `?contrato=<id>`, precarga el Contrato destino.

## Firma

```python
class CrearContratoDigital(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearContratoDigital` (`carga:crear-contrato-digital`), enlazada desde la ficha de Obra/Contrato.

## Ver también

- [ContratosDigitales](../../models/ContratosDigitales.md)
