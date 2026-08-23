---
symbol: FixBucketContentTypeForm
kind: class
module: core/forms.py
lines: 128-150
signature_hash: sha1:d1d8f30645bc6df5e7c6e4c3114819d0500982be
authored: true
---

# FixBucketContentTypeForm

**Módulo:** `core/forms.py` (líneas 128-150) · hereda de `BaseCommandRunForm`

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
