---
symbol: _invalidar_texto_solicitud
kind: function
module: secretariador/signals.py
lines: 66-67
signature_hash: sha1:97ee4da9c88d0e90cf5cb8c1d8363e4c10ce840c
authored: true
---

# _invalidar_texto_solicitud

**Módulo:** `secretariador/signals.py` (líneas 66-67)

## Propósito

Wrapper de una línea sobre [_invalidar_texto](_invalidar_texto.md) fijado a
`Solicitud`/`solicitud_texto_actuacion`, para que los receivers no repitan esos dos
argumentos en cada punto donde hace falta invalidar el texto guardado de una Solicitud.

## Firma

```python
def _invalidar_texto_solicitud(solicitud_id):
```

## Uso real

Llamado desde [invalidar_texto_actuacion_por_localidades](invalidar_texto_actuacion_por_localidades.md)
(cuando cambia el m2m `solicitud_localidades`) y desde
[invalidar_texto_actuacion_por_comisionados](invalidar_texto_actuacion_por_comisionados.md)
(cuando se crea/edita/borra un `ComisionadoSolicitud` de la Solicitud). El tercer punto de
invalidación, por cambios en los campos propios de la Solicitud, no pasa por acá: vive
directo en [invalidar_texto_actuacion_por_cambio_de_datos](invalidar_texto_actuacion_por_cambio_de_datos.md),
que ya tiene la instancia en mano dentro del `pre_save` y solo necesita poner
`instance.solicitud_texto_actuacion = None` antes de que se guarde.

## Ver también

- [_invalidar_texto](_invalidar_texto.md)
- [Solicitud](../models/Solicitud.md)
