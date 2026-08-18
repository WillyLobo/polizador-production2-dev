---
symbol: ContratoTramoPago
kind: class
module: carga/models.py
lines: 1324-1355
signature_hash: sha1:c56c78b5f0faad730aab842324870aebe5273b91
authored: true
---

# ContratoTramoPago

**Módulo:** `carga/models.py` (líneas 1324-1355) · hereda de `models.Model`

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
