---
symbol: ConcatOp
kind: class
module: personalizador/models.py
lines: 13-17
signature_hash: sha1:c681fcb719128862ec233c8c38fd0c10eef8c2c1
authored: true
---

# ConcatOp

**Módulo:** `personalizador/models.py` (líneas 13-17) · hereda de `models.Func`

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
