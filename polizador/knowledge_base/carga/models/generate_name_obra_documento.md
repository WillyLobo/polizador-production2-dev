---
symbol: generate_name_obra_documento
kind: function
module: carga/models.py
lines: 64-69
signature_hash: sha1:45d7ca3236ada108fa4d42cc9fbeb0cc040e423f
authored: true
---

# generate_name_obra_documento

**Módulo:** `carga/models.py` (líneas 64-69)

## Propósito

Callback `upload_to` de un `FileField`: Django lo llama con la instancia (todavía sin
guardar del todo) y el nombre original del archivo, y espera de vuelta la ruta relativa
donde `GCloudAndLocalStorage` (ver CLAUDE.md) va a escribirlo, tanto en GCS como en
`MEDIA_ROOT` local.

Sin partición por fecha: `documentos_obra/<obradocumento_uuid>.pdf`.

## Firma

```python
def generate_name_obra_documento(instance, filename):
```

## Uso real

`ObraDocumento.obradocumento_archivo = models.FileField(upload_to=generate_name_obra_documento, ...)` (carga/models.py:570).

## Ver también

- [ObraDocumento](ObraDocumento.md)
