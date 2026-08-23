---
symbol: GestionarTramosContrato
kind: class
module: carga/views/contratotramopagoviews.py
lines: 16-45
signature_hash: sha1:013cbe199d71bd1eb9adbc4063f92d39f65f4c92
authored: true
---

# GestionarTramosContrato

**Módulo:** `carga/views/contratotramopagoviews.py` (líneas 16-45) · hereda de `PermissionRequiredMixin, generic.View`

## Propósito

Ver [auto_increment_tramo_numero § Uso real](../../signals/auto_increment_tramo_numero.md#uso-real) — vista función-a-función (`get`/`post` explícitos, no genéricas) para el formset inline de `ContratoTramoPago` de un Contrato con certificación por etapas. Atrapa `ProtectedError` al intentar borrar un tramo que ya tiene un Certificado de Etapa generado (`on_delete=models.PROTECT` en `Certificado.certificado_contrato_tramo`) y lo muestra como mensaje de error en vez de un 500.

## Firma

```python
class GestionarTramosContrato(PermissionRequiredMixin, generic.View):
```

## Uso real

`GestionarTramosContrato` (`carga:gestionar-tramos-contrato`), enlazada desde la ficha de Contrato cuando `contrato_certificacion_por_etapas=True`.

## Ver también

- [ContratoTramoPago](../../models/ContratoTramoPago.md)
- [Contrato](../../models/Contrato.md)
- [auto_increment_tramo_numero](../../signals/auto_increment_tramo_numero.md)
