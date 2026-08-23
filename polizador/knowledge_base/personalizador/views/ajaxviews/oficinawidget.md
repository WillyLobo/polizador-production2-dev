---
symbol: oficinawidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 62-69
signature_hash: sha1:e9c603f4f7c5083149fa84a3d0d04280cdadf24e
authored: true
---

# oficinawidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 62-69) · hereda de `AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Oficina vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Busca por el nombre de cualquiera de sus cuatro niveles (Directorio/Gerencia/Dirección/Departamento). Con alta rápida (`personalizador:crear-oficina`).

## Firma

```python
class oficinawidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Agente.oficina`/`Agente.cargo_interno` en `AgenteForm`.

## Ver también

- [Oficina](../../models/Oficina.md)
