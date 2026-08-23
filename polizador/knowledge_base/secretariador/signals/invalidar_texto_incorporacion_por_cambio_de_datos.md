---
symbol: invalidar_texto_incorporacion_por_cambio_de_datos
kind: function
module: secretariador/signals.py
lines: 110-117
signature_hash: sha1:8a7da2d52dbffa360ba759720abec8e571cb64ac
authored: true
---

# invalidar_texto_incorporacion_por_cambio_de_datos

**Módulo:** `secretariador/signals.py` (líneas 110-117) · receiver de `pre_save` sobre `Incorporacion`

## Propósito

La contraparte de [invalidar_texto_actuacion_por_cambio_de_datos](invalidar_texto_actuacion_por_cambio_de_datos.md)
pero para los campos propios de `Incorporacion` en vez de los de `Solicitud`:
`incorporacion_actuacion_jurisdiccion`/`_numero`/`_ano` (`CAMPOS_TEXTO_INCORPORACION`), que
son los que arman `incorporacion_actuacion` (el `GeneratedField` que
`_calcular_texto_incorporacion` usa en el `visto_texto`). Si cambia el número de
actuación de la Incorporacion, invalida `incorporacion_texto_actuacion` para que no quede
un texto guardado que sigue mencionando el número de actuación viejo.

Los cambios en la Solicitud asociada (`incorporacion_solicitud`) — resolución, fechas,
tareas, localidades, agentes — **no** pasan por acá: esos los detecta
`invalidar_texto_actuacion_por_cambio_de_datos` (`pre_save` sobre `Solicitud`) y
[invalidar_texto_actuacion_por_comisionados](invalidar_texto_actuacion_por_comisionados.md),
que delegan en [_invalidar_incorporacion_de_solicitud](_invalidar_incorporacion_de_solicitud.md)
para propagar la invalidación hacia la Incorporacion.

## Firma

```python
def invalidar_texto_incorporacion_por_cambio_de_datos(sender, instance, **kwargs):
```

## Uso real

No se llama nunca directamente — se dispara solo en cada `Incorporacion.save()`, típicamente
desde `UpdateIncorporacion` o desde `revisar_texto_actuacion` al persistir el texto de la
incorporación (mismo mecanismo que en Solicitud: como ahí ningún otro campo cambia, el
texto recién guardado sobrevive).

## Ver también

- [_valor_comparable](_valor_comparable.md)
- [invalidar_texto_actuacion_por_cambio_de_datos](invalidar_texto_actuacion_por_cambio_de_datos.md) — misma lógica, para `Solicitud`.
- [Incorporacion](../models/Incorporacion.md)
