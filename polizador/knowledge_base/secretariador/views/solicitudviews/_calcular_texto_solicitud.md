---
symbol: _calcular_texto_solicitud
kind: function
module: secretariador/views/solicitudviews.py
lines: 19-97
signature_hash: sha1:e6e99d763c9df5adaeca9396e79358dafcb1051a
authored: true
---

# _calcular_texto_solicitud

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 19-97)

## Propósito

Arma el texto por defecto (VISTO/considerandos/artículos) de la resolución de una
Solicitud dentro del Chaco, a partir de sus datos actuales — el punto de partida que se
ofrece en `editar_texto_solicitud` y el fallback si la Solicitud todavía no tiene texto
guardado. La redacción arma listas de agentes con género correcto ("el"/"la" según
`GeneroAgente`), formatea el DNI con separador de miles a mano
(`"{:,}".format(...).replace(...)`, un workaround porque `USE_THOUSAND_SEPARATOR` con
`LANGUAGE_CODE=es-AR` no da el separador que quieren para este texto específico), y arma
la mención del vehículo/chofer si corresponde.

## Firma

```python
def _calcular_texto_solicitud(actuacion):
```

## Uso real

`_generar_solicitud_docx` (mismo módulo) y `editar_texto_solicitud` (mismo módulo), que la usa para precalcular los valores por defecto del formulario de revisión.

## Ver también

- [Solicitud](../../models/Solicitud.md)
- [_generar_solicitud_docx](_generar_solicitud_docx.md)
