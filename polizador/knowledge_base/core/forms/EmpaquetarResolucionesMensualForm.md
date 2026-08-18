---
symbol: EmpaquetarResolucionesMensualForm
kind: class
module: core/forms.py
lines: 160-197
signature_hash: sha1:8a203c6bc5ac7d195a79efab4266366af6fc7f9e
authored: true
---

# EmpaquetarResolucionesMensualForm

**Módulo:** `core/forms.py` (líneas 160-197) · hereda de `BaseCommandRunForm`

## Propósito

Año/Mes opcionales (vacíos juntos: usa el mes anterior al actual — `clean()` rechaza cargar solo uno de los dos), tamaño máximo por parte en MB, y formato a generar (ZIP/PDF/ambos).

## Firma

```python
class EmpaquetarResolucionesMensualForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["empaquetar_resoluciones_mensual"]["form"]`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
