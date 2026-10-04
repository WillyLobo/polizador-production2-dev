---
symbol: generate_name_certificados
kind: function
module: carga/models.py
lines: 30-38
signature_hash: sha1:fd6c74d9057926517d3170da934205d83e0736d8
authored: true
---

# generate_name_certificados

**Módulo:** `carga/models.py` (líneas 30-38)

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
