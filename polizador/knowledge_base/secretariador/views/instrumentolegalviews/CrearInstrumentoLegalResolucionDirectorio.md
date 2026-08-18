---
symbol: CrearInstrumentoLegalResolucionDirectorio
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 54-65
signature_hash: sha1:54721be567e4a9a1022f423d9d3da05cf88c7a7f
authored: true
---

# CrearInstrumentoLegalResolucionDirectorio

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 54-65) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de una Resolución de Directorio (`InstrumentosLegalesResolucionesDirectorioForm`, con campo de acta).

## Firma

```python
class CrearInstrumentoLegalResolucionDirectorio(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearInstrumentoLegalResolucionDirectorio` (`secretariador:crear-resolucion-directorio`).

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
