---
symbol: ConcatOp
kind: class
module: secretariador/models.py
lines: 74-78
signature_hash: sha1:225a344487f7e94fcaf0e38abd23c4f2dd235671
authored: true
---

# ConcatOp

**Módulo:** `secretariador/models.py` (líneas 74-78) · hereda de `models.Func`

## Propósito

Mismo `models.Func` mínimo que `carga.models.ConcatOp` (concatenación SQL vía `||`), redefinido acá en vez de importarse de `carga` — duplicación menor entre apps que no comparten esa utilidad. Usado para armar los campos `_str`/`_actuacion` generados por la base en varios modelos de este archivo.

## Firma

```python
class ConcatOp(models.Func):
```

## Uso real

`InstrumentosLegalesMemorandum.instrumentolegalmemorandum_str`, `InstrumentosLegalesResoluciones.instrumentolegalresoluciones_str/numero_sgt`, `Solicitud.solicitud_actuacion`, `Incorporacion.incorporacion_actuacion`, `Vehiculo.vehiculo_str` (todos `GeneratedField`).

## Ver también

- [Solicitud](Solicitud.md)
- [Vehiculo](Vehiculo.md)
