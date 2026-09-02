---
symbol: CopiarBucketDevForm
kind: class
module: core/forms.py
lines: 93-132
signature_hash: sha1:bcffd07f25477bb5fb4435d082ec577927df78c0
authored: true
---

# CopiarBucketDevForm

**Módulo:** `core/forms.py` (líneas 93-132) · hereda de `BaseCommandRunForm`

## Propósito

Expone `dry_run` (tildado por defecto — hay que destildarlo a propósito para copiar de verdad), `overwrite`, `storage_class` en destino, y `exclude_prefix` (default `pg_backup/`, para no copiar los backups de la base a dev). Deliberadamente **no** expone `--source`/`--destination`: el comando ya trae como default el único sentido autorizado (producción → dev), y aceptar nombres de bucket libres desde la web podría copiar/pisar datos en el bucket equivocado con credenciales que sí tienen permiso de escritura.

## Firma

```python
class CopiarBucketDevForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["copiar_bucket_dev"]["form"]`.

## Ver también

- [BaseCommandRunForm](BaseCommandRunForm.md)
