---
symbol: CrearContratoDigital
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 17-42
signature_hash: sha1:335ba64864ea0eb675c888d9eadf87ff980e744c
authored: true
---

# CrearContratoDigital

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 17-42) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un documento PDF adjunto a un Contrato (`ContratosDigitales`). Si viene `?contrato=<id>`, precarga el Contrato destino.

Exige el permiso propio del modelo (`carga.add_contratosdigitales`; antes pedía por error el de `certificado`). Al terminar vuelve a la ficha de la Obra del Contrato (`carga:estado-obra`), no a un listado.

## Firma

```python
class CrearContratoDigital(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearContratoDigital` (`carga:crear-contrato-digital`), enlazada desde la ficha de Obra/Contrato.

## Ver también

- [ContratosDigitales](../../models/ContratosDigitales.md)
