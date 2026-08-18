---
symbol: SyncResolucionesSgtForm
kind: class
module: core/forms.py
lines: 200-240
signature_hash: sha1:70064e2366f7f04eb5a68f6528abf4b9512de45b
authored: true
---

# SyncResolucionesSgtForm

**Módulo:** `core/forms.py` (líneas 200-240) · hereda de `BaseCommandRunForm`

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
