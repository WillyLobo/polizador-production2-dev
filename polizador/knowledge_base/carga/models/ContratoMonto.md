---
symbol: ContratoMonto
kind: class
module: carga/models.py
lines: 1347-1362
signature_hash: sha1:cdd858d141f24c6a1eafdf92583e5e316c5c1276
authored: true
---
# ContratoMonto

**Módulo:** `carga/models.py` (líneas 1347-1362) · hereda de `models.Model`

## Propósito

El monto de un Contrato desglosado por Rubro de Certificado + Financiamiento (una fila
por combinación), en pesos y UVI. Es la fuente real de dos cálculos ya cubiertos en otras
páginas: `Obra.recalcular_montos_contrato()` los suma agrupados por financiamiento para
desnormalizar el total de la Obra (ver
[recalcular_montos_obra](../signals/recalcular_montos_obra.md)), y
`PlanDeTrabajosRubro.monto_base_pesos()`/`monto_base_uvi()` usan el `ContratoMonto`
vinculado (`rubro_contratomonto`) como base para proyectar Etapas, en vez del
`rubro_presupuesto` cargado a mano.

## Firma

```python
class ContratoMonto(models.Model):
```

## Uso real

Formset inline dentro de `CrearContrato`/`UpdateContrato` (`carga/views/contratoviews.py`, `formset_name = ContratoMontoFormset`).

## Ver también

- [Contrato](Contrato.md)
- [recalcular_montos_obra](../signals/recalcular_montos_obra.md)
- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md)