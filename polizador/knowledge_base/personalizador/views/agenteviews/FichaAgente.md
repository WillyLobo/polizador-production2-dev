---
symbol: FichaAgente
kind: class
module: personalizador/views/agenteviews.py
lines: 54-81
signature_hash: sha1:d8a8afc0037bb7f392f3a0d18a2a6158bfaf787c
authored: true
---

# FichaAgente

**Módulo:** `personalizador/views/agenteviews.py` (líneas 54-81) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

La ficha principal de un Agente: precarga con `select_related`/`prefetch_related` todas
las relaciones que la plantilla recorre (título profesional, oficina y designación
temporal con sus cuatro niveles de árbol organizacional, licencias), y agrega al contexto
el balance de licencias del año actual (`resumen_agente`, función de
`personalizador/licencias.py` — fuera del alcance de este manifest, ver
[ControlLicenciasAgente](../licenciapermisoviews/ControlLicenciasAgente.md) para el mismo
patrón de uso) y los saldos de cortes de licencia pendientes, más las 10 licencias más
recientes.

## Firma

```python
class FichaAgente(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`FichaAgente` (`personalizador:ficha-agente`).

## Ver también

- [Agente](../../models/Agente.md)
- [ControlLicenciasAgente](../licenciapermisoviews/ControlLicenciasAgente.md)
