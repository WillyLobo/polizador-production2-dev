---
symbol: SyncResolucionesSgtForm
kind: class
module: core/forms.py
lines: 207-247
signature_hash: sha1:5fdd42504f07126f120c0c9d5b48db0bcfbd7f0c
authored: true
---
# SyncResolucionesSgtForm

**Módulo:** `core/forms.py` (líneas 207-247) · hereda de `BaseCommandRunForm`

## Propósito

`dry_run` (tildado por defecto), `limit` opcional (para probar con pocas antes de correr sin límite), `forzar_descarga` (ignora el último Excel exportado en caché y le pide al SGT un listado nuevo). Deliberadamente no expone `--headed` (ventana de navegador visible — no tiene sentido en un subprocess sin display en el servidor) ni `--solo-excel` (modo de depuración, no una corrida normal).

## Firma

```python
class SyncResolucionesSgtForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["sync_resoluciones_sgt"]["form"]`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)