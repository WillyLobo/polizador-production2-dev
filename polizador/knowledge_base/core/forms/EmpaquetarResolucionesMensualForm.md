---
symbol: EmpaquetarResolucionesMensualForm
kind: class
module: core/forms.py
lines: 167-204
signature_hash: sha1:001182f8cf73fcf1254fdcd9026d943220dac209
authored: true
---
# EmpaquetarResolucionesMensualForm

**Módulo:** `core/forms.py` (líneas 167-204) · hereda de `BaseCommandRunForm`

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