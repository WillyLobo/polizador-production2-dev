---
symbol: CrearAgente
kind: class
module: personalizador/views/agenteviews.py
lines: 23-40
signature_hash: sha1:7391f2bcdcd4dc71a4f5563e2e4cdd0e165a70f0
authored: true
---

# CrearAgente

**Módulo:** `personalizador/views/agenteviews.py` (líneas 23-40) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Agente vía `AgenteForm` (el más grande del módulo, ~50 campos). Usa `PopupCreateMixin` para poder abrirse como "agregar relacionado" desde cualquier `agentewidget` (ej. al elegir la autoridad a cargo de una Gerencia sin salir de ese formulario).

## Firma

```python
class CrearAgente(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearAgente` (`personalizador:crear-agente`).

## Ver también

- [Agente](../../models/Agente.md)
