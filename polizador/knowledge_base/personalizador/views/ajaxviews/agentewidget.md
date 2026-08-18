---
symbol: agentewidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 71-79
signature_hash: sha1:75ecca6c5bc9b8db30c42c5d1efecea1493c31c0
authored: true
---

# agentewidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 71-79) · hereda de `AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Versión propia de `personalizador` del widget de Agente, **con** botón "+" de alta
rápida (`AddRelatedWidgetMixin` → `personalizador:crear-agente`) — a propósito distinta
de `carga.views.ajaxviews.agentewidget` (sin ese botón), que los forms de `carga` ya
usaban antes de que existiera esta versión y siguen usando tal cual (ver el docstring de
la clase). Mismo `search_fields` (nombres/apellidos) que la de `carga`.

## Firma

```python
class agentewidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Directorio.directorio_autoridad_a_cargo_fk`, `Gerencia.gerencia_autoridad_a_cargo_fk`, `Direccion.direccion_autoridad_a_cargo_fk`, `Departamento.departamento_autoridad_a_cargo_fk`, `LicenciaPermiso.licenciapermiso_agente`.

## Ver también

- [Agente](../../models/Agente.md)
