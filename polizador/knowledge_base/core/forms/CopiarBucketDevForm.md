---
symbol: CopiarBucketDevForm
kind: class
module: core/forms.py
lines: 93-125
signature_hash: sha1:57d49108a3cca98b33ee802868a2b5fabe3f7ea4
authored: true
---

# CopiarBucketDevForm

**Módulo:** `core/forms.py` (líneas 93-125) · hereda de `BaseCommandRunForm`

## Propósito

Solo expone `dry_run` (tildado por defecto — hay que destildarlo a propósito para copiar de verdad), `overwrite`, y `storage_class` en destino. Deliberadamente **no** expone `--source`/`--destination`: el comando ya trae como default el único sentido autorizado (producción → dev), y aceptar nombres de bucket libres desde la web podría copiar/pisar datos en el bucket equivocado con credenciales que sí tienen permiso de escritura.

## Firma

```python
class CopiarBucketDevForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["copiar_bucket_dev"]["form"]`.

## Ver también

- [BaseCommandRunForm](BaseCommandRunForm.md)
