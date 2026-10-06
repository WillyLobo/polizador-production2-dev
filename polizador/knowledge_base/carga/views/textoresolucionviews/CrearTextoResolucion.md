---
symbol: CrearTextoResolucion
kind: class
module: carga/views/textoresolucionviews.py
lines: 123-130
signature_hash: sha1:0d876bd85924280cb0439e34799a76e23129ea87
authored: true
---

# CrearTextoResolucion

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 123-130) · hereda de `TextoResolucionEditorMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de una plantilla de texto de resolución. Arranca con `BLOQUES_INICIALES` (el
esqueleto habitual de una resolución del organismo: visto, considerandos, fórmula
resuelve y artículos de forma) para que el usuario no enfrente una pantalla en blanco.
Admite `?certificado=<id>` para precargar la muestra de la vista previa, que es como llega
desde la pantalla de "no hay texto base" ([_sin_plantilla](_sin_plantilla.md)). Exige
`carga.add_textoresolucioncertificado`.

## Firma

```python
class CrearTextoResolucion(TextoResolucionEditorMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`carga:crear-texto-resolucion`.

## Ver también

- [TextoResolucionEditorMixin](TextoResolucionEditorMixin.md)
- [UpdateTextoResolucion](UpdateTextoResolucion.md)
