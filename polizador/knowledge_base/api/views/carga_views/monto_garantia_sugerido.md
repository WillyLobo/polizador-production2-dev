---
symbol: monto_garantia_sugerido
kind: function
module: api/views/carga_views.py
lines: 1630-1645
signature_hash: sha1:4083fbb21422a64f7fc85ec17c307d8d2a14a3aa
authored: true
---

# monto_garantia_sugerido

**Módulo:** `api/views/carga_views.py` (líneas 1630-1645)

## Propósito

`GET /v1/api/contrato/{id}/monto-garantia/?financiamiento=&concepto=&anticipo_pct=`.
Devuelve el monto de contrato para ese financiamiento (`Contrato.monto_total`, en pesos y
en UVI) y el monto sugerido a cubrir por una garantía de ese concepto
(`Poliza.calcular_monto_a_cubrir`). Existe para la vista previa en vivo del form de Póliza
**antes de guardar**, cuando todavía no hay instancia sobre la que llamar
`monto_a_cubrir_sugerido()`. Es sólo referencia y no escribe nada. Requiere permiso sobre
`Contrato` (`require_model_perm`). Responde con el schema `GarantiaSugeridaOut`.

## Firma

```python
def monto_garantia_sugerido(request, id: int, financiamiento: str, concepto: str, anticipo_pct: Decimal=Decimal('0')):
```

## Uso real

```javascript
// carga/static/carga/js/poliza-garantia-calc.js
$.get("/v1/api/contrato/" + contratoId + "/monto-garantia/", params)
```

## Ver también

- [Poliza](../../../carga/models/Poliza.md)
- [Contrato](../../../carga/models/Contrato.md)
- [PolizaForm](../../../carga/forms/polizaforms/PolizaForm.md)
