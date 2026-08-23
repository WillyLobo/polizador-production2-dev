---
symbol: generate_name_certificados
kind: function
module: carga/models.py
lines: 29-37
signature_hash: sha1:34a7ab1305ec8178e303d620019fea6728e1338e
authored: true
---

# generate_name_certificados

**Módulo:** `carga/models.py` (líneas 29-37)

## Propósito

Callback `upload_to` de un `FileField`: Django lo llama con la instancia (todavía sin
guardar del todo) y el nombre original del archivo, y espera de vuelta la ruta relativa
donde `GCloudAndLocalStorage` (ver CLAUDE.md) va a escribirlo, tanto en GCS como en
`MEDIA_ROOT` local.

Agrupa por `certificados/<año>/<mes>/` según `certificado_fecha`, y nombra el archivo
`<certificado_uuid>_<certificado_expediente>.pdf` — el expediente en el nombre es solo
para que el archivo sea reconocible a simple vista en el bucket; la referencia real en la
base es siempre por UUID.

## Firma

```python
def generate_name_certificados(instance, filename):
```

## Uso real

`Certificado.certificado_digital = models.FileField(upload_to=generate_name_certificados, ...)` (carga/models.py:784).

## Ver también

- [Certificado](Certificado.md)
