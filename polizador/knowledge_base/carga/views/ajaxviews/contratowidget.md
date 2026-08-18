---
symbol: contratowidget
kind: class
module: carga/views/ajaxviews.py
lines: 244-248
signature_hash: sha1:f5caea657dfdbb0fb53391972fb0787494513d53
authored: false
---

# contratowidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 244-248)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class contratowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/forms/certificadoforms.py:4` — `from carga.views.ajaxviews import contratowidget, obrawidget`
- `carga/forms/certificadoforms.py:139` — `"certificado_contrato_origen":contratowidget(attrs={"class":"form-control customSelect2"}),`
- `carga/forms/documentosdigitalesforms.py:3` — `from carga.views.ajaxviews import contratowidget, obrawidget`
- `carga/forms/documentosdigitalesforms.py:17` — `"contratodigital_contrato": contratowidget(attrs={"class":"form-control customSelect2"}),`
- `carga/forms/plandetrabajosforms.py:3` — `from carga.views.ajaxviews import obrawidget, contratowidget`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
