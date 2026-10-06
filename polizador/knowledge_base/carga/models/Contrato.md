---
symbol: Contrato
kind: class
module: carga/models.py
lines: 1540-1591
signature_hash: sha1:1d50b4e5778d168f8390076716fc3d7fa877530a
authored: true
---
# Contrato

**Módulo:** `carga/models.py` (líneas 1540-1591) · hereda de `models.Model`

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

`monto_total(financiamiento_codigo, moneda)` suma todos los `ContratoMonto` del Contrato
para un financiamiento (N/P/T), en pesos o en UVI. Es la base común de los Certificados de
Etapa (`certificacion._monto_contrato_total` delega acá) y del monto de garantía sugerido
de `Poliza`.

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

- [Poliza](Poliza.md) — usa `monto_total()` para el monto de garantía sugerido.
