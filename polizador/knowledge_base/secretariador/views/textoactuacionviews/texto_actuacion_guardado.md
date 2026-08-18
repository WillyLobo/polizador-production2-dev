---
symbol: texto_actuacion_guardado
kind: function
module: secretariador/views/textoactuacionviews.py
lines: 12-13
signature_hash: sha1:b822d92fb58efd638cfe35ca1ed07d42ddf9a354
authored: true
---

# texto_actuacion_guardado

**Módulo:** `secretariador/views/textoactuacionviews.py` (líneas 12-13)

## Propósito

Helper trivial: `getattr(actuacion, texto_field_name)` — indirección para que `revisar_texto_actuacion` funcione igual sobre `solicitud_texto_actuacion` e `incorporacion_texto_actuacion` sin `if`s por tipo.

## Firma

```python
def texto_actuacion_guardado(actuacion, texto_field_name):
```

## Uso real

`revisar_texto_actuacion` (mismo módulo, más abajo).

## Ver también

- [revisar_texto_actuacion](revisar_texto_actuacion.md)
