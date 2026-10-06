---
symbol: UpdateContratoDigital
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 45-53
signature_hash: sha1:183186ce9f7f150a65fb953440e539f9ae010cde
authored: true
---

# UpdateContratoDigital

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 45-53) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un `ContratosDigitales` ya cargado.

Exige el permiso propio del modelo (`carga.change_contratosdigitales`; antes pedía por error el de `certificado`). Al terminar vuelve a la ficha de la Obra del Contrato (`carga:estado-obra`), no a un listado.

## Firma

```python
class UpdateContratoDigital(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateContratoDigital` (`carga:update-contrato-digital`).

## Ver también

- [ContratosDigitales](../../models/ContratosDigitales.md)
