---
symbol: ManualTextosResolucionView
kind: class
module: carga/views/ayudaviews.py
lines: 22-33
signature_hash: sha1:a447139f3a24fe1c49ee20affc5e2c7350f6a54d
authored: true
---

# ManualTextosResolucionView

**Módulo:** `carga/views/ayudaviews.py` (líneas 22-33) · hereda de `generic.TemplateView`

## Propósito

Manual de los textos de resolución de certificados (`ayuda/manual-textos-resolucion.html`).
A diferencia de las otras páginas de ayuda, no es del todo estática: inyecta `VARIABLES` y
`FILTROS_DOC` de `carga/resolucion_texto.py`, el mismo catálogo que alimenta la paleta del
editor. Así la tabla de variables y filtros del manual no se desactualiza cuando se agrega
una. El import está dentro del método para no cargar Jinja al importar el módulo de vistas.

## Firma

```python
class ManualTextosResolucionView(generic.TemplateView):
```

## Uso real

`carga:ayuda-textos-resolucion` (`ayuda/textos-resolucion/`), enlazada desde el menú de ayuda del navbar (`templates/navbar.html`).

## Ver también

- [TextoResolucionEditorMixin](../textoresolucionviews/TextoResolucionEditorMixin.md)
- [TextoResolucionCertificado](../../models/TextoResolucionCertificado.md)
