---
symbol: CrearInstrumentoLegalResolucionPresidencia
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 40-51
signature_hash: sha1:49e5767330d3f1f29f4ab9054c6344f29d02c6ab
authored: true
---

# CrearInstrumentoLegalResolucionPresidencia

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 40-51) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de una Resolución de Presidencia (`InstrumentosLegalesResolucionesPresidenciaForm`, sin campo de acta).

## Firma

```python
class CrearInstrumentoLegalResolucionPresidencia(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearInstrumentoLegalResolucionPresidencia` (`secretariador:crear-resolucion-presidencia`).

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
