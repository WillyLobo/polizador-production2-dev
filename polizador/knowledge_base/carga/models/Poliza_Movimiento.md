---
symbol: Poliza_Movimiento
kind: class
module: carga/models.py
lines: 264-281
signature_hash: sha1:71a50b530d9637f811bf799ee49b6ea84163f659
authored: true
---

# Poliza_Movimiento

**Módulo:** `carga/models.py` (líneas 264-281) · hereda de `models.Model`

## Propósito

Registro de que una Póliza física pasó por un Área, recibida por un Receptor, en una
fecha — el historial de "por dónde anduvo" el documento papel/expediente, independiente de
`simple_history` (que audita cambios de campos, no traslados del objeto físico).

## Firma

```python
class Poliza_Movimiento(models.Model):
```

## Uso real

Se crea junto con la Póliza en `CrearPoliza`, y se pueden agregar movimientos nuevos desde `UpdatePoliza` (`carga/views/polizaviews.py`), ambas con formset inline.

## Ver también

- [Poliza](Poliza.md)
- [Receptor](Receptor.md)
- [Area](Area.md)
