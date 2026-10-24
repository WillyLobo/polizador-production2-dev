---
symbol: sincronizar_comisionados
kind: function
module: secretariador/models.py
lines: 720-735
signature_hash: sha1:1f04cf5791b67b8f96ab4f40f2cc944072a694e5
authored: false
---

# sincronizar_comisionados

**Módulo:** `secretariador/models.py` (líneas 720-735)

## Propósito

_(pendiente de autoría)_

## Firma

```python
def sincronizar_comisionados(comisionados, recalcular_diario, motivo):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `secretariador/signals.py:5` — `from .models import ComisionadoSolicitud, Incorporacion, Solicitud, sincronizar_comisionados`
- `secretariador/signals.py:47` — `# provincia y el decreto, la tarifa diaria. Ver sincronizar_comisionados().`
- `secretariador/signals.py:203` — `sincronizar_comisionados(comisionados, pendiente["recalcular_diario"], MOTIVO_SINCRONIZAR_SOLICITUD)`
- `secretariador/signals.py:224` — `sincronizar_comisionados(comisionados, True, MOTIVO_SINCRONIZAR_INCORPORACION)`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
