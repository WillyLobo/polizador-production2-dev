---
symbol: ConjuntoLicitado
kind: class
module: carga/models.py
lines: 859-892
signature_hash: sha1:b5b1317a64be2bc391558178677e0d9cf17c4b05
authored: true
---

# ConjuntoLicitado

**Módulo:** `carga/models.py` (líneas 859-892) · hereda de `models.Model`

## Propósito

Agrupa varias Obras que salieron a licitación juntas (un "conjunto licitado"), con su
propia resolución de adjudicación. Soporta un nivel de sub-agrupamiento vía
`conjunto_subconjunto` (FK a sí mismo) — un Conjunto puede pertenecer a otro Conjunto
mayor. `conjunto_resolucion_display` sigue el mismo patrón que `Obra.obra_resolucion_display`
y `Contrato.contrato_resolucion_display`: prioriza el FK a `secretariador.InstrumentosLegalesResoluciones`
si existe, si no arma el número "legado" a mano (`RES-{año}-{numero}-{jurisdiccion}-{acta}`).

## Firma

```python
class ConjuntoLicitado(models.Model):
```

## Uso real

`CrearConjunto`/`UpdateConjunto` (`carga/views/conjuntoviews.py`); `Obra.obra_conjunto` es el FK que vincula cada Obra a su Conjunto.

## Ver también

- [Obra](Obra.md)
