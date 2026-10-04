---
symbol: UpdateTextoResolucion
kind: class
module: carga/views/textoresolucionviews.py
lines: 134-140
signature_hash: sha1:c6c7c0a595cba133f9cb0fefd4682ea387b46af1
authored: true
---

# UpdateTextoResolucion

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 134-140) · hereda de `TextoResolucionEditorMixin, PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de una plantilla existente: el formset arranca con sus `textoresolucion_bloques`.
Cambiar la plantilla **no** reescribe los snapshots ya guardados en certificados. Esos
siguen mostrando su texto hasta que se restauran o hasta que un cambio de datos los anula.
Exige `carga.change_textoresolucioncertificado`.

## Firma

```python
class UpdateTextoResolucion(TextoResolucionEditorMixin, PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`carga:update-texto-resolucion`. Es la URL de `TextoResolucionCertificado.get_absolute_url()`.

## Ver también

- [TextoResolucionEditorMixin](TextoResolucionEditorMixin.md)
- [restaurar_texto_resolucion_certificado](restaurar_texto_resolucion_certificado.md)
