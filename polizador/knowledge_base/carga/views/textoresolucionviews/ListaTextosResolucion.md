---
symbol: ListaTextosResolucion
kind: class
module: carga/views/textoresolucionviews.py
lines: 153-163
signature_hash: sha1:2feb9bd4cfd395580e2db4bd84e08783ca377dd6
authored: true
---

# ListaTextosResolucion

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 153-163) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Listado de plantillas como `ListView` plano (con `select_related` del programa) y no con
`AjaxDatatableView`: es un catálogo de unas pocas decenas de filas y no justifica el ida y
vuelta de datatables de las listas grandes. Exige `carga.view_textoresolucioncertificado`.

## Firma

```python
class ListaTextosResolucion(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`carga:lista-textos-resolucion`, destino de éxito del alta, la edición y el borrado.

## Ver también

- [TextoResolucionCertificado](../../models/TextoResolucionCertificado.md)
- [CrearTextoResolucion](CrearTextoResolucion.md)
