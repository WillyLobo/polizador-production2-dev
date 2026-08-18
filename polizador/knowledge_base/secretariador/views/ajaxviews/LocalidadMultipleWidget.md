---
symbol: LocalidadMultipleWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 33-38
signature_hash: sha1:6ee2b163ab4e1b5766991f1678404e49e786e089
authored: true
---

# LocalidadMultipleWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 33-38) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget select2 de selección múltiple — con un `search_fields` que referencia `carga.obra_nombre`/`obra_empresa`/`obra_convenio`, es decir, busca sobre campos de **Obra**, no de Localidad. Parece un widget mal nombrado/copiado de `carga.views.ajaxviews.obramultiplewidget` y nunca corregido, o efectivamente sin uso real (no se encontró ningún form de `secretariador` que la referencie — todos los que necesitan Localidad usan `carga.views.ajaxviews.localidadmultiplewidget` directamente).

## Firma

```python
class LocalidadMultipleWidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

No se encontró ningún form de `secretariador` que la use.

## Ver también

_(sin referencias cruzadas)_
