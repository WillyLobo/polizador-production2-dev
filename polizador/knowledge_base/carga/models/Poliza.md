---
symbol: Poliza
kind: class
module: carga/models.py
lines: 174-262
signature_hash: sha1:b5b7955a4757384d407f69bda2bf742f7cc82729
authored: true
---

# Poliza

**Módulo:** `carga/models.py` (líneas 174-262) · hereda de `models.Model`

## Propósito

Póliza de garantía (ejecución de contrato, sustitución de fondo de reparo, o anticipo
financiero — ver `CONCEPTO`) que una Empresa (`poliza_tomador`) presenta para una Obra
puntual. El `UniqueConstraint` sobre (fecha, número, aseguradora, tomador) es la defensa
contra carga duplicada de la misma póliza física.

**Monto de garantía sugerido.** `poliza_contrato` (el Contrato de la Obra),
`poliza_financiamiento` (N/P/T) y, sólo para el concepto `A`, `poliza_anticipo_pct` dan la
base para sugerir cuánto debería cubrir la Póliza. `calcular_monto_a_cubrir()` es un
`classmethod` puro: 5% fijo (`GARANTIA_PCT_FIJO`) del monto de contrato para los conceptos
`C`/`F`, y el % de anticipo para `A`. `monto_contrato_base()` toma esa base de
`Contrato.monto_total()` y devuelve `None` en Pólizas legacy sin Contrato/Financiamiento
(entonces no se sugiere nada). El valor es **sólo informativo**: nunca autocompleta
`poliza_monto_pesos`/`poliza_monto_uvi`.

`clean()` exige que `poliza_contrato` pertenezca a `poliza_obra`, exige
`poliza_anticipo_pct` cuando el concepto es `A` y lo pone en `None` para cualquier otro
concepto.

## Firma

```python
class Poliza(models.Model):
```

## Uso real

Se crea/edita desde `CrearPoliza`/`UpdatePoliza` (`carga/views/polizaviews.py`), junto con su primer `Poliza_Movimiento` vía formset (`FormsetViewMixin`).

El monto sugerido se muestra en la ficha (`templates/partials/ficha-poliza.html`, vía `monto_contrato_base`/`monto_a_cubrir_sugerido`) y en el listado de pólizas de la ficha de Obra. Mientras se completa el form, el endpoint `monto_garantia_sugerido` lo recalcula en vivo llamando directamente al `classmethod`:

```python
# api/views/carga_views.py (monto_garantia_sugerido)
"monto_a_cubrir_pesos": Poliza.calcular_monto_a_cubrir(concepto, monto_contrato_pesos, anticipo_pct),
```

## Ver también

- [Poliza_Movimiento](Poliza_Movimiento.md) — historial de movimientos de esta Póliza.
- [PolizaDocumento](PolizaDocumento.md) — anexos/adendas adjuntos.
- [Contrato](Contrato.md) — `monto_total()` es la base del monto sugerido.
- [monto_garantia_sugerido](../../api/views/carga_views/monto_garantia_sugerido.md)
- [Empresa](Empresa.md)
- [Aseguradora](Aseguradora.md)
