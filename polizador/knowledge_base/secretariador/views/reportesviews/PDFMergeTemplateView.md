---
symbol: PDFMergeTemplateView
kind: class
module: secretariador/views/reportesviews.py
lines: 22-24
signature_hash: sha1:30759897d5ba0467a8d0eb8ddcbc3c2b97fbb958
authored: true
---

# PDFMergeTemplateView

**Módulo:** `secretariador/views/reportesviews.py` (líneas 22-24) · hereda de `PermissionRequiredMixin, generic.TemplateView`

## Propósito

`TemplateView` sin lógica: sirve la página de la herramienta de combinar PDFs (la lógica real de merge corre client-side o vía otro endpoint, no en esta vista).

## Firma

```python
class PDFMergeTemplateView(PermissionRequiredMixin, generic.TemplateView):
```

## Uso real

`PDFMergeTemplateView` (`secretariador:pdf-merge`), enlazada desde el navbar ("Herramientas").

## Ver también

_(sin referencias cruzadas)_
