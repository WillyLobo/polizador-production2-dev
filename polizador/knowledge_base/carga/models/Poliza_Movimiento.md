---
symbol: Poliza_Movimiento
kind: class
module: carga/models.py
lines: 194-211
signature_hash: sha1:524780e24ff7d59178e35d9b345e2df51544f2d1
authored: true
---

# Poliza_Movimiento

**Módulo:** `carga/models.py` (líneas 194-211) · hereda de `models.Model`

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
