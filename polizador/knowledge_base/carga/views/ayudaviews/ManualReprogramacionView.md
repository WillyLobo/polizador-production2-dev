---
symbol: ManualReprogramacionView
kind: class
module: carga/views/ayudaviews.py
lines: 17-18
signature_hash: sha1:bca94d33dba0a68a943d57ad148862d47e9ab737
authored: true
---

# ManualReprogramacionView

**Módulo:** `carga/views/ayudaviews.py` (líneas 17-18) · hereda de `generic.TemplateView`

## Propósito

Página de ayuda estática (`ayuda/manual-reprogramacion.html`) que explica cómo reprogramar
una obra: crear el Plan nuevo con rubros que apuntan al `rubro_anterior`, cómo contar
`trabajos_meses` y cómo la matriz de Etapas completa el "hueco" de meses medidos sin
Etapa. Sólo requiere login.

## Firma

```python
class ManualReprogramacionView(generic.TemplateView):
```

## Uso real

`carga:ayuda-reprogramacion` (`ayuda/reprogramacion/`), enlazada desde el menú de ayuda del navbar (`templates/navbar.html`).

## Ver también

- [PlanDeTrabajos](../../models/PlanDeTrabajos.md)
- [PlanDeTrabajosEtapaMatriz](../plandetrabajosetapaviews/PlanDeTrabajosEtapaMatriz.md)
