---
symbol: Incorporacion
kind: class
module: secretariador/models.py
lines: 605-642
signature_hash: sha1:34505b7206a4296320ae21c5751b1b4d8252e112
authored: true
---

# Incorporacion

**Módulo:** `secretariador/models.py` (líneas 605-642) · hereda de `models.Model`

## Propósito

Incorpora agentes adicionales a una `Solicitud` ya resuelta (aprobada), con su propia
actuación electrónica y, opcionalmente, su propia resolución — sin duplicar la Solicitud
original. Sus propios `ComisionadoSolicitud` (vía
`comisionadosolicitud_incorporacion_foreign`) son *además de* los de la Solicitud
original, no un reemplazo — ver `_calcular_texto_incorporacion` en
`incorporacionviews.py`, que arma el `.docx` mencionando tanto los agentes originales
como los incorporados.

`incorporacion_texto_actuacion` es el mismo mecanismo que `Solicitud.solicitud_texto_actuacion`:
texto editado a mano que gana sobre el recién calculado si está presente. Como el texto de
una Incorporacion también depende de datos de su `incorporacion_solicitud` (resolución,
fechas, tareas, localidades, agentes originales), los receivers de
`secretariador/signals.py` invalidan `incorporacion_texto_actuacion` tanto ante cambios
propios como ante cambios en la Solicitud asociada o en sus agentes — ver
[invalidar_texto_incorporacion_por_cambio_de_datos](../signals/invalidar_texto_incorporacion_por_cambio_de_datos.md).

## Firma

```python
class Incorporacion(models.Model):
```

## Uso real

`CrearIncorporacion`/`UpdateIncorporacion` (`secretariador/views/incorporacionviews.py`).

## Ver también

- [Solicitud](Solicitud.md)
- [ComisionadoSolicitud](ComisionadoSolicitud.md)
