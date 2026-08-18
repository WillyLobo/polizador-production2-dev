---
symbol: _desglose_items_certificado
kind: function
module: carga/views/certificadoviews.py
lines: 29-79
signature_hash: sha1:852c3f802d1a014773a3cd9c9f9eb41b22775f21
authored: true
---

# _desglose_items_certificado

**Módulo:** `carga/views/certificadoviews.py` (líneas 29-79)

## Propósito

Arma, para un Certificado con Foja de origen (PARCIAL/HECHO_CONSUMADO — no ETAPA, ver
más abajo), una fila por `FojaDeMedicionItem` de esa Foja con su incidencia % fija (del
Plan de Trabajos), su acumulado anterior/mes/total, y el monto valorizado (en UVI y
pesos, convertido a la fecha del certificado) que le corresponde según esa incidencia.
Es el desglose "por qué este certificado vale lo que vale, ítem por ítem" que se muestra
en el detalle/impresión.

**ETAPA se excluye a propósito, con Foja igual**: un certificado de Etapa sí tiene
`certificado_foja` (la que disparó el tramo), pero su monto sale del % *fijo* del tramo
(`ContratoTramoPago.tramo_pct_pago`), no del avance real de esa Foja — mostrar un
desglose por ítem ahí sería engañoso, porque no es la base real de lo certificado.

## Firma

```python
def _desglose_items_certificado(certificado, contratomonto_rubro):
```

## Uso real

`_certificado_detalle_context(certificado)` (mismo módulo, más abajo).

## Ver también

- [Certificado](../../models/Certificado.md)
- [FojaDeMedicionItem](../../models/FojaDeMedicionItem.md)
- [_certificado_detalle_context](_certificado_detalle_context.md)
