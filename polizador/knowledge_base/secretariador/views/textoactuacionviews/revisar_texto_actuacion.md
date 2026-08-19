---
symbol: revisar_texto_actuacion
kind: function
module: secretariador/views/textoactuacionviews.py
lines: 29-96
signature_hash: sha1:e7fd931862b531a7d7686b0c22631744b98de31c
authored: true
---

# revisar_texto_actuacion

**Módulo:** `secretariador/views/textoactuacionviews.py` (líneas 29-96)

## Propósito

La vista GET/POST compartida por los tres flujos de generación de documento
(`solicitudviews.editar_texto_solicitud`, `solicitud_exteriorviews.editar_texto_solicitud_exterior`,
`incorporacionviews.editar_texto_incorporacion`) para revisar/editar a mano los
considerandos y artículos antes de generar el `.docx` — en vez de tres vistas casi
idénticas, cada flujo le pasa su propio texto ya calculado
(`parrafos_default`/`articulo_uno_default`/`articulo_dos_default`, con la redacción
específica de ese flujo) y esta función maneja el formulario genéricamente.

Si `EncabezadoDocumento.vigente()` es `None` (nunca se subió un encabezado base), corta
con un 500 explícito y un mensaje claro en vez de fallar más adelante al intentar generar
el `.docx` sin base. En el POST, según el botón (`accion=guardar` vs. cualquier otro),
o bien solo persiste el texto (`actuacion.save(update_fields=[texto_field_name])`) y
vuelve a la ficha, o guarda y redirige a la URL de generación del `.docx` del flujo
correspondiente (`generar_docx_url_name`, parametrizado por el caller).

En el GET, el valor inicial de cada campo del formulario sale de
`texto_actuacion_guardado(actuacion, texto_field_name)` si la actuación ya tiene texto
guardado (`solicitud_texto_actuacion`/`incorporacion_texto_actuacion`), y de los
`*_default` recién calculados si no. Para `articulo_dos` la elección es por fila
(`_articulo_dos_inicial`, mismo módulo): toma como base la lista *actual* de agentes
comisionados y solo reutiliza la fila guardada de los que siguen estando; un agente nuevo
aparece con su valor recién calculado, uno eliminado simplemente desaparece. Para
`parrafos`/`articulo_uno` no hay ese tipo de reconciliación fila a fila — es todo el texto
guardado o todo el recién calculado. Por eso `solicitud_texto_actuacion`/
`incorporacion_texto_actuacion` necesitan invalidarse activamente cuando cambian los
datos que el texto describe (agentes, fechas, localidades, vehículo, resolución
referenciada): si no, esta vista seguiría prellenando el formulario con un texto guardado
desactualizado en vez de reflejar el cambio. Ese es el trabajo de los receivers en
`secretariador/signals.py` (ver
[invalidar_texto_actuacion_por_cambio_de_datos](../../signals/invalidar_texto_actuacion_por_cambio_de_datos.md)
y las demás señales del módulo) — ponen el campo en `None` para que el próximo GET caiga
en la rama `*_default`.

## Firma

```python
def revisar_texto_actuacion(request, *, actuacion, texto_field_name, generar_docx_url_name, parrafos_default, articulo_uno_default, articulo_dos_default, extra_context=None):
```

## Uso real

```python
# secretariador/views/solicitudviews.py (editar_texto_solicitud)
return revisar_texto_actuacion(
    request, actuacion=actuacion, texto_field_name="solicitud_texto_actuacion",
    generar_docx_url_name="secretariador:crear-documento-solicitud",
    parrafos_default=parrafos_default, articulo_uno_default=articulo_uno_default,
    articulo_dos_default=articulo_dos_default,
)
```

## Ver también

- [EncabezadoDocumento](../../models/EncabezadoDocumento.md)
- [editar_texto_solicitud](../solicitudviews/editar_texto_solicitud.md)
- [editar_texto_solicitud_exterior](../solicitud_exteriorviews/editar_texto_solicitud_exterior.md)
- [editar_texto_incorporacion](../incorporacionviews/editar_texto_incorporacion.md)
- [invalidar_texto_actuacion_por_cambio_de_datos](../../signals/invalidar_texto_actuacion_por_cambio_de_datos.md) — mantiene sincronizado el texto que esta vista prellena.
