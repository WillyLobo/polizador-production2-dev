---
symbol: FixBucketContentTypeForm
kind: class
module: core/forms.py
lines: 135-157
signature_hash: sha1:44c8445debfa19a291573e92ee4d2df1ba3b330b
authored: true
---
# FixBucketContentTypeForm

**Módulo:** `core/forms.py` (líneas 135-157) · hereda de `BaseCommandRunForm`

## Propósito

`dry_run` (tildado por defecto) + `prefix` opcional para acotar la corrección. Mismo motivo que `CopiarBucketDevForm` para no exponer `--bucket`: el comando ya usa como default el único bucket pensado para esto.

## Firma

```python
class FixBucketContentTypeForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["fix_bucket_content_type"]["form"]`.

## Ver también

- [CopiarBucketDevForm](CopiarBucketDevForm.md)