---
symbol: ConcatOp
kind: class
module: personalizador/models.py
lines: 12-16
signature_hash: sha1:e8576f2eadc68b7830a5fc8bae93ffb31a9cb7b3
authored: true
---

# ConcatOp

**Módulo:** `personalizador/models.py` (líneas 12-16) · hereda de `models.Func`

## Propósito

`models.Func` mínimo para concatenar strings en SQL vía `||` (el operador de
concatenación estándar SQL/Postgres) en vez de `django.db.models.functions.Concat` —
probablemente porque `Concat` no encajaba con `GeneratedField`/`db_persist=True` de la
forma que necesitaban estos campos, o simplemente porque se escribió antes de que el
proyecto adoptara `Concat` en otros lados. Usado exclusivamente para construir campos
generados por la base (nombre completo, número de actuación) que se recalculan solos en
cada `INSERT`/`UPDATE`.

## Firma

```python
class ConcatOp(models.Func):
```

## Uso real

`Agente.agente_nombreyapellido`/`agente_apellidoynombre_coma`, `ComisionadoExterno.agente_nombreyapellido`, `CorteLicencia.cortelicencia_nota_actuacion` (todos `GeneratedField`).

## Ver también

- [Agente](Agente.md)
- [CorteLicencia](CorteLicencia.md)
