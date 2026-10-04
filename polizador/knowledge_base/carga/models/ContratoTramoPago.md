---
symbol: ContratoTramoPago
kind: class
module: carga/models.py
lines: 1593-1624
signature_hash: sha1:8f53b1648589d40ce3271549d5235272d4def394
authored: true
---
# ContratoTramoPago

**Módulo:** `carga/models.py` (líneas 1593-1624) · hereda de `models.Model`

## Propósito

Un tramo de pago fijo de un Contrato con `contrato_certificacion_por_etapas=True`:
`tramo_pct_pago` es el % del Contrato que se certifica cuando este tramo se dispara, y
`tramo_pct_disparador` es el umbral de % de avance acumulado (de la Foja) que lo habilita.
`tramo_numero` es correlativo por Contrato, auto-asignado por
[auto_increment_tramo_numero](../signals/auto_increment_tramo_numero.md) — el más simple
de los tres patrones de auto-numeración del módulo (sin cadena de reprogramación).

## Firma

```python
class ContratoTramoPago(models.Model):
```

## Uso real

`GestionarTramosContrato` (`carga/views/contratotramopagoviews.py:35`), formset inline sobre un Contrato.

## Ver también

- [Contrato](Contrato.md)
- [Certificado](Certificado.md) — `certificado_contrato_tramo` es el `OneToOneField` que salda un Tramo.
- [auto_increment_tramo_numero](../signals/auto_increment_tramo_numero.md)