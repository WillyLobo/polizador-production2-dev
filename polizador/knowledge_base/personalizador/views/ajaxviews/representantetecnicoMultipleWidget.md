---
symbol: representantetecnicoMultipleWidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 8-12
signature_hash: sha1:e3b701bd00c60e2d1a725a9ef0bd8976f0336a63
authored: true
---

# representantetecnicoMultipleWidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 8-12) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget select2 (`django-select2`) para elegir uno o más RepresentanteTecnico vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Selección múltiple, busca por nombre y apellido.

## Firma

```python
class representantetecnicoMultipleWidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

`Obra.obra_representantetecnico` en `carga.forms.obraforms.ObraForm`.

## Ver también

- [RepresentanteTecnico](../../models/RepresentanteTecnico.md)
