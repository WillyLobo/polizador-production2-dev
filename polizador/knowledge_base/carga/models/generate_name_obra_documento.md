---
symbol: generate_name_obra_documento
kind: function
module: carga/models.py
lines: 56-61
signature_hash: sha1:decb708d9620071ae3414ced1d5f4ae8fff6bdea
authored: true
---

# generate_name_obra_documento

**Módulo:** `carga/models.py` (líneas 56-61)

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
