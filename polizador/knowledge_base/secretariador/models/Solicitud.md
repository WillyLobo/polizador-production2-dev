---
symbol: Solicitud
kind: class
module: secretariador/models.py
lines: 392-458
signature_hash: sha1:6317ef1e666e53593883f6a8ac8099c94b9421dd
authored: true
---

# Solicitud

**Módulo:** `secretariador/models.py` (líneas 392-458) · hereda de `models.Model`

## Propósito

El modelo central de `secretariador`: una solicitud de comisión de servicio (viáticos),
identificada por una actuación electrónica (`solicitud_actuacion`, `GeneratedField` que
concatena jurisdicción-año-número-AE, con dos `UniqueConstraint` distintas — una sobre el
campo generado completo, otra sobre sus tres partes por separado, redundantes entre sí
pero ambas declaradas). `solicitud_cantidad_de_dias` es otro `GeneratedField`: la resta de
fechas calculada por la base de datos, no en Python.

`get_absolute_url` bifurca según la Provincia: si es "Chaco", va a la edición de Solicitud
normal; si no, a la edición de Solicitud Exterior — son la misma tabla, dos flujos/vistas
de edición distintos según si el viaje es dentro o fuera de la provincia (ver
`solicitudviews.py` vs `solicitud_exteriorviews.py`).

`solicitud_texto_actuacion` guarda el texto de considerandos/artículos editado a mano
desde la web (ver `textoactuacionviews.py`); si está vacío, el `.docx` se genera con el
texto calculado automáticamente a partir de los datos de la solicitud. Los receivers de
`secretariador/signals.py` ponen este campo en `None` automáticamente apenas cambian los
datos de la Solicitud que ese texto describe (agentes, fechas, localidades, vehículo),
para que no quede desactualizado respecto de un texto guardado antes del cambio — ver
[invalidar_texto_actuacion_por_cambio_de_datos](../signals/invalidar_texto_actuacion_por_cambio_de_datos.md).

## Firma

```python
class Solicitud(models.Model):
```

## Uso real

`CrearSolicitud`/`UpdateSolicitud` (`secretariador/views/solicitudviews.py`), `CrearSolicitudExterior`/`UpdateSolicitudExterior` (`secretariador/views/solicitud_exteriorviews.py`).

## Ver también

- [ComisionadoSolicitud](ComisionadoSolicitud.md)
- [InstrumentosLegalesResoluciones](InstrumentosLegalesResoluciones.md)
- [Incorporacion](Incorporacion.md)
