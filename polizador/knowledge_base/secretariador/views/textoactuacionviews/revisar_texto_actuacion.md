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
