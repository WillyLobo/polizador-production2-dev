---
symbol: Contrato
kind: class
module: carga/models.py
lines: 1272-1312
signature_hash: sha1:604de6103e2764c477c2b13eab7c9240fcad90de
authored: true
---
# Contrato

**Módulo:** `carga/models.py` (líneas 1272-1312) · hereda de `models.Model`

## Propósito

El contrato de obra (legal/administrativo) de una Obra — puede haber más de uno a lo
largo del tiempo (`contrato_vigente()` en `Obra` toma el más reciente, mismo patrón que
`plan_vigente()`). `contrato_resolucion_display` sigue el mismo patrón que
`Obra.obra_resolucion_display`/`ConjuntoLicitado.conjunto_resolucion_display`.

El campo con más impacto en el resto del sistema es
`contrato_certificacion_por_etapas`: si está tildado, esta Obra **no** genera
certificados PARCIAL (%mes de la Foja) — en su lugar, certifica en tramos fijos de %
disparados cuando el avance acumulado de la Foja alcanza el umbral de cada
`ContratoTramoPago`. Es la bifurcación central que decide si `certificacion.py` construye
certificados PARCIAL o ETAPA para esta Obra.

## Firma

```python
class Contrato(models.Model):
```

## Uso real

`CrearContrato`/`UpdateContrato` (`carga/views/contratoviews.py`), con el formset inline de `ContratoMonto`.

## Ver también

- [Obra](Obra.md)
- [ContratoTramoPago](ContratoTramoPago.md) — solo relevante cuando `contrato_certificacion_por_etapas=True`.
- [ContratoMonto](ContratoMonto.md)
- [Certificado](Certificado.md) — tipos PARCIAL vs ETAPA.