---
symbol: Poliza
kind: class
module: carga/models.py
lines: 160-192
signature_hash: sha1:22b3a5ba9a934b5d36dd5d2b390b1e0513a36bf0
authored: true
---

# Poliza

**Módulo:** `carga/models.py` (líneas 160-192) · hereda de `models.Model`

## Propósito

Póliza de garantía (ejecución de contrato, sustitución de fondo de reparo, o anticipo
financiero — ver `CONCEPTO`) que una Empresa (`poliza_tomador`) presenta para una Obra
puntual. El `UniqueConstraint` sobre (fecha, número, aseguradora, tomador) es la defensa
contra carga duplicada de la misma póliza física.

## Firma

```python
class Poliza(models.Model):
```

## Uso real

Se crea/edita desde `CrearPoliza`/`UpdatePoliza` (`carga/views/polizaviews.py`), junto con su primer `Poliza_Movimiento` vía formset (`FormsetViewMixin`).

## Ver también

- [Poliza_Movimiento](Poliza_Movimiento.md) — historial de movimientos de esta Póliza.
- [Empresa](Empresa.md)
- [Aseguradora](Aseguradora.md)
