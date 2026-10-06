---
symbol: TextoResolucionEditorMixin
kind: class
module: carga/views/textoresolucionviews.py
lines: 42-119
signature_hash: sha1:84d02fbefebc513d92b0287b6c6eb0e007c34eae
authored: true
---

# TextoResolucionEditorMixin

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 42-119)

## Propósito

GET/POST compartido por el alta y la edición de plantillas: el form de alcance
([TextoResolucionForm](../../forms/textoresolucionforms/TextoResolucionForm.md)), el formset
de bloques (`BloqueFormSet`, prefijo `bloques`) y el panel de vista previa contra un
certificado de muestra ([CertificadoMuestraForm](../../forms/textoresolucionforms/CertificadoMuestraForm.md)).
Las subclases sólo definen `view_type`, `title` y `bloques_iniciales()`.

En el `post` se validan **siempre** los tres forms (sin `and` encadenado), para que la
página vuelva con todos los errores marcados juntos. Si llega `accion=previsualizar` y el
formset es válido, re-renderiza con la vista previa sin guardar. Si no, guarda el form con
`commit=False`, le asigna `formset.bloques_validos()` a `textoresolucion_bloques` y
redirige al listado.

La vista previa es un POST normal que re-renderiza la página, no htmx: es el mismo ida y
vuelta del resto del sistema y se testea con `self.client.post`. htmx está cargado en
`base.html`, pero ninguna plantilla lo usa todavía y no hay un patrón de CSRF establecido.
`get_context_data` agrega `VARIABLES`/`FILTROS_DOC` para la paleta del editor.

## Firma

```python
class TextoResolucionEditorMixin:
```

## Uso real

Base de [CrearTextoResolucion](CrearTextoResolucion.md) y [UpdateTextoResolucion](UpdateTextoResolucion.md).

## Ver también

- [_previsualizar](_previsualizar.md)
- [BaseBloqueFormSet](../../forms/textoresolucionforms/BaseBloqueFormSet.md)
- [TextoResolucionCertificado](../../models/TextoResolucionCertificado.md)
- [ManualTextosResolucionView](../ayudaviews/ManualTextosResolucionView.md)
