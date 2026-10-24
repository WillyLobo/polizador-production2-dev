---
symbol: _campos_que_se_guardan
kind: function
module: secretariador/signals.py
lines: 73-78
signature_hash: sha1:40da4b119c4112d2a8a04471fea6331d24faeacf
authored: false
---

# _campos_que_se_guardan

**Módulo:** `secretariador/signals.py` (líneas 73-78)

## Propósito

_(pendiente de autoría)_

## Firma

```python
def _campos_que_se_guardan(model, campos, update_fields):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `secretariador/signals.py:172` — `campos_dias = _campos_que_se_guardan(Solicitud, CAMPOS_DIAS_SOLICITUD, update_fields)`
- `secretariador/signals.py:173` — `campos_tarifa = _campos_que_se_guardan(Solicitud, CAMPOS_TARIFA_SOLICITUD, update_fields)`
- `secretariador/signals.py:211` — `if not instance.pk or not _campos_que_se_guardan(Incorporacion, ["incorporacion_solicitud_id"], update_fields):`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
