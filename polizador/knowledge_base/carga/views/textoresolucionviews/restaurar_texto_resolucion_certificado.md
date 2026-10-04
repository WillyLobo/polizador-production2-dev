---
symbol: restaurar_texto_resolucion_certificado
kind: function
module: carga/views/textoresolucionviews.py
lines: 286-292
signature_hash: sha1:87a1661a32b06866a97eb4f63d6d376c9f972330
authored: true
---

# restaurar_texto_resolucion_certificado

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 286-292)

## Propósito

Descarta el snapshot editado a mano de un Certificado (`certificado_texto_resolucion=None`)
para que el texto se vuelva a resolver desde la plantilla vigente. Sólo actúa por POST, usa
`.update()` (para no dejar una fila de historial ni disparar señales del modelo) y siempre
vuelve a la pantalla de revisión. Exige `carga.change_certificado`.

## Firma

```python
def restaurar_texto_resolucion_certificado(request, pk):
```

## Uso real

`carga:restaurar-texto-resolucion-certificado`, botón "Restaurar desde la plantilla" de la pantalla de revisión cuando se está viendo un snapshot.

## Ver también

- [editar_texto_resolucion_certificado](editar_texto_resolucion_certificado.md)
- [invalidar_texto_resolucion_por_cambio_de_datos](../../signals/invalidar_texto_resolucion_por_cambio_de_datos.md) — el descarte automático cuando cambian los datos.
